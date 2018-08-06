SETTING UP KEMA MASTERNODE:
===========================
* First set up a VPS server. We recommend VULTR.COM
* Set up an account, and verify your email.

### Setting up your Masternode.

* From your page at vultr.com Click on the "plus" sign to add server.
* Server type choose Ubuntu 1604 x64
* Select the 25GB SSD
* Label the Server MN1 (for masternode 1 and so on.)
* Once deployed copy the IP address to the clipboard
 
To access your server we recommend using PUTTY. 
Download Putty at http://www.putty.org

### Run Putty
* Paste server address under session into Host Name (or IP address) section
* Enter the server name "MN1" in the name block and click save
* press the open button
* When Security Alert box opens, click Yes
* Enter Username and Password

If you need to run updates use this:

    apt update && apt upgrade -y && reboot

After all updates and upgrades completed, close window

Restart PuTTY, choose the session you just created the copy both lines below, right click in PuTTY.

    wget https://raw.githubusercontent.com/wmcorless/kema/master/mn-setup.sh
    bash mn-setup.sh

It will run on its own after right clicking.
Once completed running it will ask for private key (just hit the return key) 
It will then say "kema server starting" will be displayed and a new key will be generated.

When program finishes highlight complete line starting with "MN#". Once highlighted it will be copied into your clipboard.
Now click on tools of your Kema Coin Wallet and then open Masternode configuration file.

Paste the line you just copied into the Masternode Configuration file,
Change # sign to latest number of the node.  CTRL "S" to save file.
run debug console in wallet, "getaccountaddress MN#" --copy address generated and paste into
the address box under Send.

### Send 5000 coins

Open Transactions and click on "Payment to yourself"
RIGHT CLICK and copy TXID #. 
You will then paste it in Masternode config file one space after
MN# line.  CTRL S and save the file.  Go back to the Debug Console and run the below command.

    masternode outputs

it will then give you a listing of all transaction ID's of your Masternodes.  
Compare the last four digits of each ID.  
The last digit of each line will be a 1 or a 0 (zero).  
Now enter that digit at the end of the line following a blank space.  DO NOT HIT THE ENTER KEY.  
That digit has to be the last character in the config file or your Node will not run.  
Now close the configuration file and close the Kema Wallet program.  
Once program has closed, it will take 15-30 seconds before all files are written.  
Restart the wallet.  Once wallet is in sync open Masternodes Highlight the node you just created.  
You can either click on "Start alias" or "Start MISSING" to ENABLE the newly created Masternode.

Now we have to check if it is running on the server, to do so copy the below command and right click in your open session of PuTTY.  
Hit the enter key.

    kema-cli masternode status

The last line should read: "status" : "Masternode successfully started".  It will take 10-15 minutes before the Active column shows 
progress. If the minutes are a minus then you got synced but and asks for action to be completed, check your Masternode configuration 
file to be sure there are no extra lines, spaces or carriage returns after the last line.
You may now close your PuTTY session and you are ready to create another server and start another node if desired.
