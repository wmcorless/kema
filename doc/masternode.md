SETTING UP KEMA MASTERNODE:
===========================
* First set up a VPS server. We recommend Digital Ocean.
* Set up an account, and verify your email.

### Setting up your VPS

* Add server.
* Server type choose Ubuntu 18.04 x64
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

Use our new ubuntu setup guide https://github.com/wmcorless/kema/blob/master/doc/Ubuntu%2020.04%20Build.md

# Setting up your Masternode using your Wallet
Now in the Kema Coin Wallet click on Tools > Masternode configuration file.

If you are using notepad you should see an example line starting with a `#`. This is a comment line.
It is recommended that you name each of your masternodes as MN1, MN2, etc.
Change # sign to 1 or the latest number of the node.  
CTRL "S" to save file.
In the wallet click Tools > Debug to go to the console 
Type:

    getaccountaddress MN1
    
Copy address generated. This is the addresss we are going to send the collateral to.

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

Make sure you have enough confirmations and it will then give you a listing of all transaction ID's of your Masternodes.  
Compare the first three digits of each ID to find the one you just created.  
The last digit of each line will be a 1 or a 0 (zero).  
Now enter that digit at the end of the line following a blank space. 
Your config line should not have any "enter" keys on the line just spaces seperating each item. 
The number has to be the last character in the config file or your Node will not run.  
Make sure the config file follows the same nomenclature as the example provided.
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
