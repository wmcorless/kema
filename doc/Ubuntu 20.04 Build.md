UNIX BUILD NOTES
====================
Some notes on how to build Kemacoin Core On a ubuntu 20.04 server from root.

## Linux Distribution Specific Instructions

### Ubuntu & Debian

#### Dependency Build Instructions

Update you're installation:

    apt update; apt upgrade -y; apt autoremove -y


Build requirements:

    sudo apt-get install build-essential libtool bsdmainutils autotools-dev autoconf pkg-config automake python3 -y

You need to add the following dependency:

    echo 'deb http://security.ubuntu.com/ubuntu bionic-security main' >> /etc/apt/sources.list

Update the cache:

    sudo apt update && apt-cache policy libssl1.0-dev
    
Install dependencies.

    sudo apt-get install libssl1.0-dev libgmp-dev libevent-dev libboost-all-dev libsodium-dev cargo -y
    

BerkeleyDB is required for the wallet.

    sudo add-apt-repository ppa:pivx/pivx

Update the system.

    sudo apt-get update
    sudo apt-get install libdb4.8-dev libdb4.8++-dev -y
    

Optional port mapping libraries (see: `--with-miniupnpc`, and `--enable-upnp-default`, `--with-natpmp`, `--enable-natpmp-default`):

    sudo apt install libminiupnpc-dev libnatpmp-dev -y
    

ZMQ dependencies (provides ZMQ API):

    sudo apt-get install libzmq3-dev -y
    

Install Boost

    wget https://boostorg.jfrog.io/artifactory/main/release/1.65.1/source/boost_1_65_1.tar.gz
    tar -xzf boost_1_65_1.tar.gz
    cd boost_1_65_1
    ./bootstrap.sh
    ./b2
    ./b2 install
    cd
    rm boost_1_65_1.tar.gz
    rm boost_1_65_1 -r
    
Add Paths

    PATH=$PATH:~/usr/local/lib
    export LD_LIBRARY_PATH=/usr/local/lib
    echo 'export PATH=$PATH:~/usr/local/lib' >> ~/.bashrc
    echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib' >> ~/.bashrc

Add Dpendencies:

    wget https://github.com/wmcorless/kema/releases/download/v1.0.0.5/dependencies.tar.gz
    tar -xzf dependencies.tar.gz
    mv -t /usr/lib/x86_64-linux-gnu/ libboost_system.so.1.65.1 libminiupnpc.so.10

GUI dependencies:

If you want to build kema-qt, make sure that the required packages for Qt development
are installed. Qt 5 is necessary to build the GUI.
To build without GUI pass `--without-gui`.

To build with Qt 5 you need the following:

    sudo apt-get install libqt5gui5 libqt5core5a libqt5dbus5 libqt5svg5-dev libqt5charts5-dev qttools5-dev qttools5-dev-tools libqrencode-dev

You can either download the binaries or you can build from source.

Download Binaries
---------------------
```bash
wget https://github.com/wmcorless/kema/releases/download/v1.0.0.5/kema-linux-binaries.tar.gz
tar -xzf kema-linux-binaries.tar.gz
mv -t /usr/local/bin kemad kema-cli
rm kema-linux-binaries.tar.gz
```
or

Build from source
---------------------
    
```bash
git clone https://github.com/wmcorless/kema.git
cd kema
./autogen.sh
```
```bash
./configure --with-boost-libdir=/usr/local/lib/
make
strip src/kemad src/kema-cli
make install # optional
```

This will build kema-qt as well, if the dependencies are met.
