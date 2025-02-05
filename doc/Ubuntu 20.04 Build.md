UNIX BUILD NOTES
====================
Some notes on how to build Kemacoin Core On a ubuntu 20.04 server from root.
if working with less than 2GB memory it is advised to set up a swap file. See https://www.digitalocean.com/community/tutorials/how-to-add-swap-space-on-ubuntu-20-04

## Linux Distribution Specific Instructions

### Ubuntu & Debian

#### Dependency Build Instructions

Update you're installation:

    apt update; apt upgrade -y; apt autoremove -y

Build requirements:

    sudo apt-get install build-essential libtool bsdmainutils autotools-dev autoconf pkg-config automake python3 -y

You need to add the following dependency:

    echo 'deb [trusted=yes] http://security.ubuntu.com/ubuntu bionic-security main' >> /etc/apt/sources.list

Update the cache:

    sudo apt update && apt-cache policy libssl1.0-dev
    
Install dependencies.

    sudo apt-get install libssl1.0-dev libgmp-dev libevent-dev libboost-all-dev libsodium-dev cargo -y

BerkeleyDB is required for the wallet.

    sudo apt-get install software-properties-common
    sudo add-apt-repository ppa:pivx/berkeley-db4

Update the system.

    sudo apt-get update
    sudo apt-get install libdb4.8-dev libdb4.8++-dev -y

Optional port mapping libraries (see: `--with-miniupnpc`, and `--enable-upnp-default`, `--with-natpmp`, `--enable-natpmp-default`):

    sudo apt install libminiupnpc-dev libnatpmp-dev -y

ZMQ dependencies (provides ZMQ API):

    sudo apt-get install libzmq3-dev -y

Install Boost

    wget https://archives.boost.io/release/1.65.1/source/boost_1_65_1.tar.gz
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

# Download Binaries

```bash
wget https://github.com/wmcorless/kema/releases/download/v1.0.0.5/kema-linux-binaries.tar.gz
tar -xzf kema-linux-binaries.tar.gz
mv -t /usr/local/bin kemad kema-cli
rm kema-linux-binaries.tar.gz
```
or

# Build from source
When building from source we recommend 2GB of ram since compilers are memory intensive. Adding a swapfile is also recommended.
    
```bash
git clone https://github.com/wmcorless/kema.git
cd kema
./autogen.sh
```
```bash
./configure --with-boost-libdir=/usr/local/lib/ CXXFLAGS="--param ggc-min-expand=1 --param ggc-min-heapsize=32768" 
make
strip src/kemad src/kema-cli
make install # optional
```

Masternode setup
----
One of the things that is important with running a masternode is fault tolerance. If your masternode goes down you want to have the system immediately restart it. We can accomplish this with `systemctrl`. We will now create a systemctrl for our new server.

```bash
nano /etc/systemd/system/kema.service
```
Paste the following text:

    [Unit]
    Description=kema service
    After=network.target

    [Service]
    User=root
    Group=root

    Type=forking
    #PIDFile=/root/.kema/kema.pid

    ExecStart=/usr/local/bin/kemad -daemon -conf=/root/.kema/kema.conf -datadir=/root/.kema
    ExecStop=/usr/local/bin/kema-cli -conf=/root/.kema/kema.conf -datadir=/root/.kema stop

    Restart=always
    PrivateTmp=true
    TimeoutStopSec=60s
    TimeoutStartSec=10s
    StartLimitInterval=120s    
    StartLimitBurst=5

    [Install]
    WantedBy=multi-user.target

Save the file and run the following lines to activate it.

    systemctl daemon-reload
    systemctl start kema.service
    systemctl enable kema.service >/dev/null 2>&1

You can now start your server with:

    systemctl start kema.service

You can stop it with:

    systemctl stop kema.service

Now we will edit the config file.

    nano .kema/kema.conf

Paste the following in the editor:

    rpcuser=<your rpcuser>
    rpcpassword=<your password>
    rpcallowip=127.0.0.1
    listen=1
    server=1
    daemon=0
    port=65075
    logintimestamps=1
    maxconnections=256
    masternode=1
    externalip=<your ip>:65075
    masternodeprivkey=<paste your masternode key here>
    addnode=161.97.88.199
    addnode=164.92.230.144
    addnode=46.151.159.53
    addnode=138.68.17.33
    addnode=165.22.177.156	
    addnode=158.140.182.237
    addnode=135.181.211.44
    addnode=50.123.3.124
    addnode=74.82.154.237	
    addnode=64.226.83.248
    addnode=167.99.226.193

Make sure that you change the username and password to secure your server. Also add your IP address and Masternode Key. If you need assistance setting up your masternode check out the documentation section.
