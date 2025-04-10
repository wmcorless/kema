# Linearize
Construct a linear, no-fork, best version of the blockchain.

## Step 1:
Edit example-linearize.cfg

Required configuration file settings for linearize-hashes:
* RPC: rpcuser, rpcpassword:
* Optional config file setting for linearize-hashes:
* RPC: host, port
* Block chain: min_height, max_height

## Step 2:
Copy the config file:

    cp example-linearize.cfg linearize.cfg

## Step 3: Download hash list

    python3 linearize-hashes.py linearize.cfg > hashlist.txt

## Step 2: Copy local block data

    python3 linearize-data.py linearize.cfg

Required configuration file settings:
* "input": kemad blocks/ directory containing blkNNNNN.dat
* "hashlist": text file containing list of block hashes, linearized-hashes.py
output.
* "output_file": bootstrap.dat
      or
* "output": output directory for linearized blocks/blkNNNNN.dat output

Optional config file setting for linearize-data:
* "netmagic": network magic number
* "max_out_sz": maximum output file size (default 1000*1000*1000)
* "split_timestamp": Split files when a new month is first seen, in addition to
reaching a maximum file size.
* "file_timestamp": Set each file's last-modified time to that of the
most recent block in that file.
