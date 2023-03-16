SETTING UP KEMA MASTERNODE:
===========================
* First set up a VPS server. We recommend Digital Ocean.
* Set up an account, and verify your email.

### Setting up your VPS

* Add server.
* Server type choose Ubuntu 1604 x64
* Select the 25GB SSD
* Label the Server MN1 (for masternode 1 and so on.)
* Once deployed copy the IP address to the clipboard
 
To access your server we recommend using PUTTY. 
Download Putty at http://www.putty.org

### Run PuTTY
* Paste server address under session into Host Name (or IP address) section
* Enter the server name "MN1" in the saved sessions and click save
* Press the open button
* When Security Alert box opens, click Yes
* Enter Username and Password

If you need to run updates use this:

    apt update && apt upgrade -y && reboot

After all updates and upgrades completed, close window

Restart puTTY, choose the session you just created.
Log in to server and copy the following:

    wget https://raw.githubusercontent.com/wmcorless/kema/master/mn-setup.sh -O mn-setup.sh
    bash mn-setup.sh

Paste in your prompt and press enter or simply right clicking.
Once completed running it will ask for a private key (just hit the return key) 
It will then say "kema server starting" will be displayed and a new key will be generated.

When program finishes highlight complete line starting with "MN#". 
Once highlighted it will be copied into your clipboard.
Now in the Kema Coin Wallet click on Tools > Masternode configuration file.

On a blank line paste the line you just copied into the Masternode Configuration file.
Change # sign to 1 or the latest number of the node.  
CTRL "S" to save file.
In the wallet click Tools > Debug to go to the console 
Type:

    getaccountaddress MN1
    
Copy address generated.

### Send Collateral

* Click the send tab.
* Paste the address you created in the previous step in the "Pay to:" block
You should see MN1 appear in the "Label" to confirm you have done this correctly.
Enter 5000 coins for the required collateral in the amount and press send.

Open Transactions and you should see the transaction you created.
Double click on "Payment to yourself" to open a window.
Double click on the txid number to highlight it, then copy it. 
Go back to your masternode config file and then paste it in Masternode config file one space after MN# line.  
CTRL S and save the file.  
Go back to the Debug Console and run the below command.

    masternode outputs

It will then give you a listing of all transaction ID's of your Masternodes.  
Compare the first three digits of each ID to find the one you just created.  
The last digit of each line will be a 1 or a 0 (zero).  
Now enter that digit at the end of the line following a blank space. 
Your config line should not have any "enter" keys on the line just spaces seperating each item. 
The number has to be the last character in the config file or your Node will not run.  
Now save and close the configuration file and close the Kema Wallet program.  

### Start Masternode

* Restart the wallet and wait for it to sync.  
* Make sure your sent transaction has at least 17 confirmations
* Select Masternode Tab and select the node you just created.  
* Click on "Start Alias"  button to ENABLE the newly created Masternode.
* If everything has been done correctly it should say "Enabled".

### Verify Masternode is Running

* Open puTTY
* log into your server.
* At the Prompt enter the following:

    kema-cli masternode status

The last line should read: "status" : "Masternode successfully started".  
You may now close your PuTTY session and you are ready to create another server and start another node if desired.
If your server says "In Sync: Waiting for remote Activation" repeat Start Masternode again.
If you have any questions or need assistance visit us at Discord.
