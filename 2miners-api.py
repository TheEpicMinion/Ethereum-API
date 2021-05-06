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
                    "url": "https://eth.2miners.com/account/" + ethereumAdress,
                    "icon_url": "https://2miners.com/i/about-page/2m_logotype_ver.png",
                },
                "description": "**Current Hashrate: **" + hashrateCurrent + " MH/s\n**Average Hashrate: **" + hashrateAverage + " MH/s",
                "fields": [
                    {
                        "name": "Workers",
                        "value": "Online: **" + workerOnline + "** Offline: **" + workerOffline + "** Total: **" + workerTotal + "**\n" + workerStr,
                        "inline": True
                    },
                    {
                        "name": "Rewards",
                        "value": sumReward0 + "\n" + sumReward1 + "\n" + sumReward2,
                        "inline": True
                    },
                    {
                        "name": "Payouts",
                        "value": "Paid: **" + balancePaid + "**\nUnpaid: **" + balanceUnpaid + "**\n Progress: **" + progress +  "**%",
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

    url = "https://eth.2miners.com/api/accounts/" + ethereumAdress

    response = urllib.request.urlopen(url)

    data = json.loads(response.read())

    # Retrieve reward value from JSON
    sumReward0 = data["sumrewards"][0]["reward"]
    sumReward1 = data["sumrewards"][1]["reward"]
    sumReward2 = data["sumrewards"][2]["reward"]

    # Clear last 3 char and add string
    sumReward0 = "**01h: **" + str(sumReward0)[:-3] + "µ ETH"
    sumReward1 = "**12h: **" + str(sumReward1)[:-3] + "µ ETH"
    sumReward2 = "**24h: **" + str(sumReward2)[:-3] + "µ ETH"

    # Retrieve worker value from JSON
    workerAmount = data["workers"]

    # initialize/reset the counter
    i = 0

    # Loop throug every worker name
    for key in json.loads(json.dumps(workerAmount)):
        if i < 30: 
                    # Save the status of the worker
                    workerStatus = (data["workers"][key]["offline"])

                    # Check the status emoji
                    if workerStatus == False:
                        workerEmoji = ":white_check_mark:"
                    else:
                        workerEmoji = ":x:"
        
                    # Add the worker to the list
                    workerStr = str(workerStr + ("*" + key + "*: " + workerEmoji + "\n"))
        # Up one the counter
        i = i + 1

    # Retrieve hashrates from JSON
    hashrateCurrent = str(data["currentHashrate"])
    hashrateAverage = str(data["hashrate"])

    # Clear last chars
    hashrateCurrent = hashrateCurrent[:-4]
    hashrateCurrent = spacer(hashrateCurrent, ".")

    hashrateAverage = hashrateAverage[:-4]
    hashrateAverage = spacer(hashrateAverage, ".")

    # Retrieve amount of workers from JSON
    workerOffline = str(data["workersOffline"])
    workerOnline = str(data["workersOnline"])
    workerTotal = str(data["workersTotal"])

    # Retrieve unpaid balance from JSON
    balanceUnpaid = str(data["stats"]["balance"])[:-5]

    if int(balanceUnpaid) < 10:
        balanceUnpaid = "0.000" + balanceUnpaid
    elif int(balanceUnpaid) < 100:
        balanceUnpaid = "0.00" + balanceUnpaid
    elif int(balanceUnpaid) < 1000:
        balanceUnpaid = "0.0" + balanceUnpaid
    else:
        balanceUnpaid = "0." + balanceUnpaid

    # Retrieve paid balance from JSON
    balancePaid = str(data["stats"]["paid"])[:-6]
    if int(balancePaid) < 1000:
        balancePaid = "0.0" + str(balancePaid)
    else :
        balancePaid = str(balancePaid)[:-3] + "." + str(balancePaid)[(len(str(balancePaid))-3):]

    # Calculate progress amount
    progress = str(float(balanceUnpaid) / 0.05 * 100)

    # Send the discord Webhook
    discordWebhook()

    time.sleep(delay)