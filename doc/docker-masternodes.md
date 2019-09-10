SETTING UP MASTERNODES IN DOCKER:
===========================
* First set up a VPS server. We recommend Amazon Web Services or Digital Ocean.
* Set up an account, and verify your email.

### Setting up your VPS

How to create multiple masternodes per VPS with docker.  This document was put together by Dave Winings, and Bill Corless. 
If you want to help support them use the links for Digital Ocean.
Sign up for Digital Ocean receive $50 in credits. Use one of the links below.

Bill Corless https://m.do.co/c/6b4b07a4667e \
David Winings https://m.do.co/c/8445d58c96ff

With Digital Ocean we have found that if you use the $20 server you can get up to 28 masternodes on it.

We recommend using the latest version ubuntu server.

First run the following in your VPS while in root:

    apt update 
    apt install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
Once that is done you want to add the docker key:

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
Now add the docker repository:

    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
Update and install files:

    apt update
    apt install docker-ce docker-ce-cli containerd.io

Test the installation:

    docker run hello-world

Edit docker daemon.json

    nano /etc/docker/daemon.json

Paste the following into the screen

    {
      "ipv6": true,
      "fixed-cidr-v6": "2001:db8:1::/64"
    }

Exit nano with ctrl-x "y" enter

Setup forwarding and ip -6 route

    ip -6 route add 2001:db8:1::/64 dev docker0
    sysctl net.ipv6.conf.default.forwarding=1
    sysctl net.ipv6.conf.all.forwarding=1 
    ip6tables -t nat -A POSTROUTING -s 2001:db8:1::/64 -j MASQUERADE

Setup Network:

    docker network create --subnet=172.18.0.0/16 mynet123
    docker run --net mynet123 --ip 172.18.0.22 -it ubuntu:16.04

You should now be in the container, type: 

    exit
    
Next we setup a new ubuntu 16.04 container:

    docker run -it --privileged --cap-add=NET_ADMIN --restart always --name mn ubuntu:16.04 /bin/bash

This will put you in the container, now enter the following:

    cd
    apt update && apt upgrade -y
    apt install nano wget lsb-core net-tools iptables dbus -y
When this is finished we will download and install the masternode script:

    wget https://raw.githubusercontent.com/wmcorless/kema/master/mn-setup.sh -O mn-setup.sh
    bash mn-setup.sh

When it asks for the masternode key just press enter, we are going to do this later.

We want to start the Masternode with:

    kemad -daemon
It will take some time for the Masternode to sync up. To check the status use:

    kema-cli masternode status
Make sure your masternode is in sync. Once synchronized exit container with:

    ctrl-p ctrl-q 
Next we will start the registry locally.

    docker run -d -p 5000:5000 --restart always --name registry registry:2
Now list your images with:

    docker ps
Copy the container label for masternode and place it in the line below:

    docker commit [container label] masternode
    
Now list docker images with:

    docker images
    
Copy the tag for the id for masternode and place it in the line below:

    docker image tag [id] localhost:5000/masternode
Now we push and pull it:

    docker push localhost:5000/masternode
    docker pull localhost:5000/masternode
    
### Setup your first Masternode:

    docker run -dit --restart always --name mn1 localhost:5000/masternode
    
You will need to set the Masternode key for each node by editing the kema.conf file.
Here is an example:

    docker attach mn1
    cd /root/.kema
    nano kema.conf
Replace the masternode key with the correct one. Save the file and exit.

Then run the Kema daemon from the VPS root with:

    docker exec -it mn1 kemad -daemon
You can change the name for each of the masternodes as appropriate.

To connect to individual containers use:
    docker attach mn1

### Setting up cron to automatically load all of your masternodes.

First we want create a bash file that will run the commands that start your nodes.

    nano start.sh
If you have 2 masternodes for example enter the following into your Bash file:

    #!/bin/bash
    docker exec -d mn1 kemad -daemon
    docker exec -d mn2 kemad -daemon
Add additional lines as needed.

Save your file and make it executable:

    chmod +x start.sh

To test the file use: 

    ./start.sh
If it works good edit your crontab with the following:

    crontab -e
The first time you use it select Nano.  Add the following to the bottom of the file:

    @reboot sleep 30; /root/start.sh
Test your system by rebooting and use "top" to see what files are running.

    top
You should see the COMMAND "kemad" loaded for each container.

### Some helpful docker commands
Stop all containers:

    docker stop $(docker ps -a -q)
Remove all stopped containers:

    docker rm $(docker ps -a -q)
Remove all unused images:

    docker system prune -a 
