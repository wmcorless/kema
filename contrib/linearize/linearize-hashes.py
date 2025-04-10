#!/usr/bin/env python3
"""
bootstrap-kemacoin.py: Retrieve full blocks from the Kemacoin node via RPC and produce a
bootstrap data file (bootstrap.dat) to speed up initial blockchain sync.

Usage:
  python bootstrap-kemacoin.py linearize.cfg

The configuration file (linearize.cfg) should contain lines such as:
    rpcuser=youruser
    rpcpassword=yourRPCpass
    host=127.0.0.1
    port=16745               # Adjust to your Kemacoin RPC port
    min_height=0
    use_https=False          # Optional: set to True if your node uses HTTPS
    netmagic=697c2446        # 8 hex characters representing your Kemacoin network magic
    output=bootstrap.dat     # (optional) output file name
    max_blocks_per_call=100  # (optional) batch size for RPC calls
"""

import json
import re
import base64
import http.client
import sys
import struct

# Global settings dictionary (populated from config file)
settings = {}

class KemacoinRPC:
    def __init__(self, host, port, username, password, use_https=False):
        self.use_https = use_https
        authpair = "{}:{}".format(username, password)
        # In Python 3, base64.b64encode returns bytes, so we decode it.
        self.authhdr = "Basic " + base64.b64encode(authpair.encode("utf-8")).decode("utf-8")
        if self.use_https:
            self.conn = http.client.HTTPSConnection(host, port, timeout=300)
        else:
            self.conn = http.client.HTTPConnection(host, port, timeout=300)

    def execute(self, request_array):
        """
        Execute a batch of JSON-RPC requests.
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
            print("JSON parse error: {}. Raw response: {}".format(e, body), file=sys.stderr)
            sys.exit(1)
        return resp_obj

    @staticmethod
    def build_request(idx, method, params):
        """
        Build a JSON-RPC request object.
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
        Check whether the response object indicates an error.
        """
        return ('error' in resp_obj) and (resp_obj['error'] is not None)

def write_bootstrap(settings, max_blocks_per_call=100):
    # Establish RPC connection.
    use_https = settings.get('use_https', False)
    rpc = KemacoinRPC(settings['host'], settings['port'],
                      settings['rpcuser'], settings['rpcpassword'],
                      use_https=use_https)

    # Step 1: Get current chain tip.
    batch_for_count = [rpc.build_request(0, 'getblockcount', [])]
    reply_count = rpc.execute(batch_for_count)
    if not reply_count or len(reply_count) < 1:
        print("Error: getblockcount failed", file=sys.stderr)
        sys.exit(1)
    if rpc.response_is_error(reply_count[0]):
        print("Error: getblockcount returned error: {}".format(reply_count[0]['error']), file=sys.stderr)
        sys.exit(1)
    current_tip = reply_count[0]['result']
    print("Current chain tip is: {}".format(current_tip), file=sys.stderr)

    # Start at min_height (default is 0).
    start_height = settings.get('min_height', 0)
    print("Starting from block height: {}".format(start_height), file=sys.stderr)

    # Step 2: Validate network magic.
    magic_hex = settings.get('netmagic')
    if magic_hex is None:
        print("Error: 'magic' or 'netmagic' must be set in configuration (8 hex characters)", file=sys.stderr)
        sys.exit(1)
    if len(magic_hex) != 8:
        print("Error: 'magic/netmagic' must be 8 hex characters", file=sys.stderr)
        sys.exit(1)
    try:
        # In Python 3, use bytes.fromhex()
        magic_bytes = bytes.fromhex(magic_hex)
    except Exception as e:
        print("Error decoding magic hex: {}".format(e), file=sys.stderr)
        sys.exit(1)

    # Step 3: Open the output file.
    output_file = settings.get('output', 'bootstrap.dat')
    try:
        out_f = open(output_file, "wb")
    except Exception as e:
        print("Error opening output file: {}".format(e), file=sys.stderr)
        sys.exit(1)

    # Step 4: Iterate over blocks and write them to the bootstrap file.
    height = start_height
    total_blocks = 0
    while height <= current_tip:
        num_blocks = min(current_tip - height + 1, max_blocks_per_call)
        # Batch RPC: get block hashes for the current batch.
        batch_hashes = []
        for x in range(num_blocks):
            batch_hashes.append(rpc.build_request(x, 'getblockhash', [height + x]))
        reply_hashes = rpc.execute(batch_hashes)
        if not reply_hashes or len(reply_hashes) < num_blocks:
            print("Error: batch RPC call for getblockhash didn't return enough items", file=sys.stderr)
            sys.exit(1)
        block_hashes = []
        for x, resp_obj in enumerate(reply_hashes):
            if rpc.response_is_error(resp_obj):
                print("Error at height {}: {}".format(height+x, resp_obj['error']), file=sys.stderr)
                sys.exit(1)
            block_hashes.append(resp_obj['result'])

        # Batch RPC: retrieve full block data (hex string) for each block hash.
        batch_blocks = []
        for idx, bh in enumerate(block_hashes):
            # getblock with verbose=false returns block data as a hex string.
            batch_blocks.append(rpc.build_request(idx, 'getblock', [bh, False]))
        reply_blocks = rpc.execute(batch_blocks)
        if not reply_blocks or len(reply_blocks) < num_blocks:
            print("Error: batch RPC call for getblock didn't return enough items", file=sys.stderr)
            sys.exit(1)
        # Process each block and write it in bootstrap format.
        for x, resp_obj in enumerate(reply_blocks):
            if rpc.response_is_error(resp_obj):
                print("Error fetching block at height {}: {}".format(height+x, resp_obj['error']), file=sys.stderr)
                sys.exit(1)
            block_hex = resp_obj['result']
            try:
                block_bin = bytes.fromhex(block_hex)
            except Exception as e:
                print("Error decoding block hex at height {}: {}".format(height+x, e), file=sys.stderr)
                sys.exit(1)
            block_size = len(block_bin)
            # Write 4-byte network magic, 4-byte block length (little-endian), then the block data.
            out_f.write(magic_bytes)
            out_f.write(struct.pack("<I", block_size))
            out_f.write(block_bin)
            total_blocks += 1
            if (total_blocks % 10) == 0:
                print("Processed block at height {}".format(height+x), file=sys.stderr)
        height += num_blocks

    out_f.close()
    print("Bootstrap file created successfully with {} blocks in {}".format(total_blocks, output_file), file=sys.stderr)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: bootstrap-kemacoin.py CONFIG-FILE", file=sys.stderr)
        sys.exit(1)

    # Load configuration from the config file.
    cfg_file = sys.argv[1]
    try:
        with open(cfg_file, "r") as f:
            for line in f:
                # Skip comment lines.
                if re.search(r'^\s*#', line):
                    continue
                m = re.search(r'^(\w+)\s*=\s*(\S.*)$', line)
                if m is None:
                    continue
                key = m.group(1)
                val = m.group(2)
                if key in ['port', 'min_height', 'max_height', 'max_blocks_per_call']:
                    try:
                        settings[key] = int(val)
                    except ValueError:
                        print("Error: {} must be an integer".format(key), file=sys.stderr)
                        sys.exit(1)
                elif key == 'use_https':
                    settings[key] = val.lower() in ['true', '1', 'yes']
                else:
                    settings[key] = val.strip()
    except Exception as e:
        print("Error reading config file: {}".format(e), file=sys.stderr)
        sys.exit(1)

    # Set defaults if necessary.
    if 'host' not in settings:
        settings['host'] = '127.0.0.1'
    if 'port' not in settings:
        settings['port'] = 16745
    if 'min_height' not in settings:
        settings['min_height'] = 0
    if 'rpcuser' not in settings or 'rpcpassword' not in settings:
        print("Missing rpcuser/rpcpassword in config", file=sys.stderr)
        sys.exit(1)

    max_blocks = settings.get('max_blocks_per_call', 100)
    write_bootstrap(settings, max_blocks)
