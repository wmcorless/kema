UNIX BUILD NOTES
====================
Some notes on how to build Kemacoin Core in Unix.

On a ubuntu 20.04 - 22.04 server from root

## Linux Distribution Specific Instructions

### Ubuntu & Debian

#### Dependency Build Instructions

Build requirements:

    sudo apt-get install build-essential libtool bsdmainutils autotools-dev autoconf pkg-config automake python3

Edit this file /etc/apt/sources.list and add this line to the end of it.

    deb http://security.ubuntu.com/ubuntu bionic-security main

After that run:

    sudo apt update && apt-cache policy libssl1.0-dev
    
Finally,

    sudo apt-get install libssl1.0-dev
    
Then

    sudo apt-get install libgmp-dev libevent-dev libboost-all-dev libsodium-dev cargo

BerkeleyDB is required for the wallet.

    sudo apt-get install software-properties-common
    sudo add-apt-repository ppa:pivx/pivx
    
    sudo apt-get update
    sudo apt-get install libdb4.8-dev libdb4.8++-dev
    
    git clone https://github.com/wmcorless/kema.git

Optional port mapping libraries (see: `--with-miniupnpc`, and `--enable-upnp-default`, `--with-natpmp`, `--enable-natpmp-default`):

    sudo apt install libminiupnpc-dev libnatpmp-dev

ZMQ dependencies (provides ZMQ API):

    sudo apt-get install libzmq3-dev

GUI dependencies:

If you want to build kema-qt, make sure that the required packages for Qt development
are installed. Qt 5 is necessary to build the GUI.
To build without GUI pass `--without-gui`.

To build with Qt 5 you need the following:

    sudo apt-get install libqt5gui5 libqt5core5a libqt5dbus5 libqt5svg5-dev libqt5charts5-dev qttools5-dev qttools5-dev-tools libqrencode-dev

To Build
---------------------
    
```bash
cd kema
./autogen.sh
./configure
make
make install # optional
```

This will build kema-qt as well, if the dependencies are met.
