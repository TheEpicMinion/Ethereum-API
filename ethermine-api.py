import urllib.request
import json
import requests
import time

# This is a script written for the Ethereum cryptocurrency on the 2miners pool
# All you need to do is fill in your Discord Webhooklink on line 18, your ethereumAdress on line 21,
# And the time of interval in seconds on line 24.

# Now just run the program and everything should be ready to go.
# Bugs can be reported to 'Epic Minion#5253'

# Consider buying me a coffee
# Ethereum: 0xECB542Cf182Eb4B0A1a7B81Fb2113E833FeEb017
# Bitcoin: bc1qtmmlhlmdezre2ur3xvqlnv9kdcjw8ejfmsk3jc

# Insert Discord Webhook here
discordWebhookURL = ""

# Insert Ethereum adress here

ethereumAdress = ""

# Insert time in seconds to wait between messages
delay = 1800

def spacer(message, char):
    posistion = len(message) - 2
    message = message[:posistion] + char + message[posistion:]
    return message

def discordWebhook():
    url = discordWebhookURL
    payload = {
        "embeds": [
            {
                "author": {
                    "name": ethereumAdress,
                    "url": "https://ethermine.org/miners/" + ethereumAdress,
                    "icon_url": "https://static.netify.ai/logos/e/t/h/rgurezvar/icon.png?v=1",
                },
                "description": "**Current Hashrate: **" + hashrateCurrent + " MH/s\n**Reported Hashrate: **" + hashrateReported + " MH/s",
                "fields": [
                    {
                        "name": "Workers",
                        "value": "Online: **" + workerAmount + "**\n" + workerStr,
                        "inline": True
                    },
                    {
                        "name": "Shares",
                        "value": "Valid: **" + sharesValid + "**\nInvalid: **" + sharesInvalid + "**\nStale: **" + sharesStale + "**",
                        "inline": True
                    },  
                    {
                        "name": "Balance",
                        "value": "Unpaid: **" + balanceUnpaid + "** ETH",
                        "inline": True
                    }
                ],
            }
        ]
    }
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, json=payload, headers=headers)

while(True):
    workerStr = ""

    url = "https://api.ethermine.org/miner/" + ethereumAdress + "/dashboard"
    headers = {
	    "cookie": "pmuser_country=be",
	    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0"
	}
    response = requests.request("GET", url, headers=headers).json()

    # Retrieve unpaid value from DICT
    unpaid = response["data"]["currentStatistics"]["unpaid"]

    # Clear last 12 char and add DICT
    unpaid = str(unpaid)[:-12] + "\xb5 ETH"

    # Retrieve hashrates from DICT
    hashrateCurrent = str(int((response["data"]["currentStatistics"]["currentHashrate"])))
    hashrateReported = str(int((response["data"]["currentStatistics"]["reportedHashrate"])))

    # Clear last chars
    hashrateCurrent = hashrateCurrent[:-4]
    hashrateCurrent = spacer(hashrateCurrent, ".")

    hashrateReported = hashrateReported[:-4]
    hashrateReported = spacer(hashrateReported, ".")

    # Retrieve worker value from DICT
    workerAmount = response["data"]["currentStatistics"]["activeWorkers"]

    # initialize/reset the counter
    i = 0
    j = 0

    # Add Variables
    start = 0
    end = workerAmount
    step = 1

    # Loop throug every worker name
    for item in range(start,end,step):
        if i <= 30:
            # name of the worker
            workerName = response["data"]["workers"][i]["worker"]
            workerReported = str(int(response["data"]["workers"][i]["reportedHashrate"]))
            workerAverage = str(int(response["data"]["workers"][i]["currentHashrate"]))

            # Clear last chars
            workerAverage = workerAverage[:-4]
            workerAverage = spacer(workerAverage, ".")

            workerReported = workerReported[:-4]
            workerReported = spacer(workerReported, ".")


            workerStr = str(workerStr + ("*" + workerName + ":* " + str(workerAverage) + " MH | " + str(workerReported) + " MH\n"))

            # Up one the counter
            i = i + 1

    # Chaning int to string
    workerAmount = str(workerAmount)

    # Retrieve amount of shares from DICT
    sharesValid = str(response["data"]["currentStatistics"]["validShares"])
    sharesInvalid = str(response["data"]["currentStatistics"]["invalidShares"])
    sharesStale = str(response["data"]["currentStatistics"]["staleShares"])

    # Retrieve unpaid balance from JSON
    balanceUnpaid = str(response["data"]["currentStatistics"]["unpaid"])
    balanceUnpaid = balanceUnpaid[:-14]

    if int(balanceUnpaid) < 100:
        balanceUnpaid = "0.00" + balanceUnpaid
    elif int(balanceUnpaid) < 1000:
        balanceUnpaid = "0.0" + balanceUnpaid
    elif int(balanceUnpaid) < 10000:
        balanceUnpaid = "0." + balanceUnpaid
    else:
        balanceUnpaid = "0." + balanceUnpaid

    # Send the discord Webhook
    discordWebhook()

    time.sleep(delay)