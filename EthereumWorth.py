import urllib.request
import json
import requests
from datetime import datetime
import time as t
import pylint

# This is a script written for current price of the Ethereum cryptocurrency
# All you need to do is fill in your Discord Webhooklink on line 22, your Etherscan API on line 25,
# And the time of interval in seconds on line 28

# The Etherscan API key isn't necessarry if you don't set the time under 5 sec

# Now just run the program and everything should be ready to go.
# Bugs can be reported to 'Epic Minion#5253'

# Consider buying me a coffee
# Ethereum: 0xECB542Cf182Eb4B0A1a7B81Fb2113E833FeEb017
# Bitcoin: bc1qtmmlhlmdezre2ur3xvqlnv9kdcjw8ejfmsk3jc

# Insert Discord Webhook here
discordWebhookURL = ""

# Insert etherscan.io API key here, you can get one here https://etherscan.io/myapikey/
apikey = ""

# Insert time in seconds to wait between messages
delay = 3600

def discordWebhook():
    url = discordWebhookURL
    payload = {
        "embeds": [
            {
                "author": {
                    "name": titleStr + " | " + str(worthUSD) + "$",
                    "url": "https://etherscan.io",
                    "icon_url": "https://cryptologos.cc/logos/ethereum-eth-logo.png",
                },
                "description": "Proposed gas: **" + gasPricePropose + "**gwei | Fast gas: **" + gasPriceFast + "**gwei",
                "color": color
            }
        ]
    }
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, json=payload, headers=headers)

worthUSDPrev = 1

while(True):
    # Etherium price API
    url_price = "https://api.etherscan.io/api?module=stats&action=ethprice&apikey=" + apikey
    response = urllib.request.urlopen(url_price)
    data = json.loads(response.read())

    # Etherium gas API
    gas_url = "https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=" + apikey
    gas_response = urllib.request.urlopen(gas_url)
    gas = json.loads(gas_response.read())

    # Get the worth in USD from JSON
    worthUSD = float(data["result"]["ethusd"])

    # Check what embed color it gets
    if worthUSD <= worthUSDPrev : 
        color = 16711680 # Price went down
    else : 
        color = 65280 # Price went up

    # Get the timestamp from JSON
    timestamp = int(data["result"]["ethusd_timestamp"])
    time = datetime.fromtimestamp(timestamp)

    # Calculating the percantage
    if worthUSD < worthUSDPrev : 
        # Price went down
        percentage = (worthUSD / worthUSDPrev) * 100
        percentage = round(100 - percentage, 2) * -1

        titleStr = "PRICE DROPPED: " + str(percentage) + "%"

    else :  
        # Price went up
        percentage = worthUSD / worthUSDPrev * 100
        percentage = round(percentage - 100, 2)

        titleStr = "PRICE ROSE: " + str(percentage) + "%"

    # Get the average gas price from JSON
    gasPricePropose = gas["result"]["ProposeGasPrice"]
    gasPriceFast = gas["result"]["FastGasPrice"]

    # Only send if there is a change and when the program isn't running for the first time
    if percentage != 0.0 and worthUSDPrev != 1:
        # Send the discord Webhook
        discordWebhook()

    # Set the new price as the old one for next time
    worthUSDPrev = worthUSD

    t.sleep(delay)
