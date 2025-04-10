#!/usr/bin/env python3
"""
linearize-kemacoin.py: List blocks in a linear, no-fork version of the Kemacoin chain,
from min_height up to the chain tip using the JSON-RPC API.

Usage:
  python linearize-kemacoin.py linearize.cfg > kemacoin_blocks.txt

The configuration file (linearize.cfg) might contain lines like:
    rpcuser=youruser
    rpcpassword=yourRPCpass
    host=127.0.0.1
    port=65076
    min_height=0
    use_https=False

Make sure your Kemacoin node is running with RPC enabled.
"""

import json
import re
import base64
import http.client
import sys

# Global settings dictionary
settings = {}

class KemacoinRPC:
    def __init__(self, host, port, username, password, use_https=False):
        self.use_https = use_https
        authpair = f"{username}:{password}"
        # In Python3, base64.b64encode returns bytes so decode it to get a string.
        self.authhdr = "Basic " + base64.b64encode(authpair.encode("utf-8")).decode("utf-8")
        if self.use_https:
            self.conn = http.client.HTTPSConnection(host, port, timeout=300)
        else:
            self.conn = http.client.HTTPConnection(host, port, timeout=300)

    def execute(self, request_array):
        """
        Makes one batch RPC call with request_array (a list of JSON-RPC requests).
        """
        self.conn.request(
            'POST',
            '/',
            json.dumps(request_array),
            {
                'Authorization': self.authhdr,
                'Content-type': 'application/json'
            }
        )

        resp = self.conn.getresponse()
        if resp is None:
            print("JSON-RPC: no response", file=sys.stderr)
            return None

        body = resp.read()
        try:
            resp_obj = json.loads(body)
        except ValueError as e:
            print(f"JSON parse error: {e}", file=sys.stderr)
            print(f"Raw response body: {body}", file=sys.stderr)
            sys.exit(1)
        return resp_obj

    @staticmethod
    def build_request(idx, method, params):
        """
        Build a JSON-RPC request object. We use the common "jsonrpc": "1.0" for many
        Bitcoin-derived coins like Kemacoin.
        """
        return {
            'jsonrpc': '1.0',
            'id': idx,
            'method': method,
            'params': params if params is not None else []
        }

    @staticmethod
    def response_is_error(resp_obj):
        """
        Check if an individual response object indicates an error.
        """
        return ('error' in resp_obj) and (resp_obj['error'] is not None)

def get_block_hashes(settings, max_blocks_per_call=1000):
    """
    Retrieve block hashes from the Kemacoin node starting at min_height and going up
    to the chain tip. Prints each block hash to stdout in ascending order.
    """
    use_https = settings.get('use_https', False)
    rpc = KemacoinRPC(settings['host'], settings['port'],
                      settings['rpcuser'], settings['rpcpassword'],
                      use_https=use_https)

    # Step 1: Get the current chain tip using getblockcount.
    batch_for_count = [rpc.build_request(0, 'getblockcount', [])]
    reply_count = rpc.execute(batch_for_count)
    if not reply_count or len(reply_count) < 1:
        print("Error: getblockcount failed, no reply", file=sys.stderr)
        sys.exit(1)
    if rpc.response_is_error(reply_count[0]):
        print(f"Error: getblockcount returned an error: {reply_count[0]['error']}", file=sys.stderr)
        sys.exit(1)

    current_tip = reply_count[0]['result']
    print(f"Current chain tip is: {current_tip}", file=sys.stderr)

    # Start fetching from min_height (defaulting to 0 if not provided).
    height = settings.get('min_height', 0)
    print(f"Starting from block height: {height}", file=sys.stderr)

    # Step 2: Loop until we reach the chain tip.
    while height <= current_tip:
        num_blocks = min(current_tip - height + 1, max_blocks_per_call)
        batch = []
        for x in range(num_blocks):
            # Build a "getblockhash" request for block at height + x.
            batch.append(rpc.build_request(x, 'getblockhash', [height + x]))

        reply = rpc.execute(batch)
        if not reply or len(reply) < num_blocks:
            print("Error: batch RPC call didn't return enough items", file=sys.stderr)
            sys.exit(1)

        # Step 3: Process each response and print the block hash.
        for x, resp_obj in enumerate(reply):
            if rpc.response_is_error(resp_obj):
                print(f"JSON-RPC error at height {height + x}: {resp_obj['error']}", file=sys.stderr)
                sys.exit(1)
            # Confirm that the response id is what we expected.
            assert resp_obj['id'] == x, "Mismatched response id"
            print(resp_obj['result'])

        height += num_blocks

    print(f"Finished. Last height fetched was {current_tip}", file=sys.stderr)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: linearize-kemacoin.py CONFIG-FILE", file=sys.stderr)
        sys.exit(1)

    # Parse the configuration file.
    cfg_file = sys.argv[1]
    with open(cfg_file) as f:
        for line in f:
            # Skip comment lines.
            if re.search('^\s*#', line):
                continue

            # Parse key=value formatted lines.
            m = re.search('^(\w+)\s*=\s*(\S.*)$', line)
            if m is None:
                continue
            key = m.group(1)
            val = m.group(2)

            if key in ['port', 'min_height', 'max_height']:
                settings[key] = int(val)
            elif key == 'use_https':
                # Configure boolean value for use_https.
                settings[key] = val.lower() in ['true', '1', 'yes']
            else:
                settings[key] = val

    # Set defaults if not provided in the config.
    if 'host' not in settings:
        settings['host'] = '127.0.0.1'
    if 'port' not in settings:
        # Set this default to the typical Kemacoin RPC port if desired.
        settings['port'] = 65076
    if 'min_height' not in settings:
        settings['min_height'] = 0

    if 'rpcuser' not in settings or 'rpcpassword' not in settings:
        print("Missing rpcuser/rpcpassword in config", file=sys.stderr)
        sys.exit(1)

    # Run the block hash fetching routine.
    get_block_hashes(settings, max_blocks_per_call=1000)
