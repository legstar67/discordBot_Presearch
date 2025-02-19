import discord
import subprocess
from datetime import datetime
import requests

import botTools

API_KEY = '34118050-405b-44d4-a201-3233e1b6b730' #TODO WARNING it's private key

async def handle_docker_logs(message, command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    botTools.sd_msg('Starting to stream logs...')

    while True:
        output = process.stdout.readline()
        if output == '' :#and process.poll() is not None:
            break
        if output:
            await botTools.send_message(message.channel, output.strip())

    await message.channel.send('Log streaming ended.')



#return a list where each element is a line of the logs
def parseLogsDocker(logs):
    list = []
    sizeLogs = len(logs)
    seperator = "\n"
    sizeSeperator = len(seperator)
    index = 0
    tempFind = 0

    while index < sizeLogs and index >= 0:
        print(index)
        tempFind = logs[index:].find(seperator)
        list.append(
            logs[index:tempFind if tempFind>0 else sizeLogs]
            )
        index = tempFind + sizeSeperator

    return list

# transfer the logs of docker on the server , to the program 
# TODO maybe command docker to not need to wait to have logs starting 
async def getLogsDocker(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    botTools.sd_msg('Starting to stream logs...')

    while True:
        output = process.stdout.readline()
        if output == '' :#and process.poll() is not None:
            break
        if output:
            await botTools.send_message(message.channel, output.strip())


def get_crypto_price(symbol):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': symbol,
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY
    }
 
    try:
        response = requests.get(url, headers=headers, params=parameters)
        response.raise_for_status()
        data = response.json()

        if symbol in data['data'] and 'quote' in data['data'][symbol] and 'USD' in data['data'][symbol]['quote']:
            price = data['data'][symbol]['quote']['USD']['price']
            return price
        else:
            print(f"Données non valides pour le symbole {symbol}.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête API : {e}")
        return None
    except KeyError as e:
        print(f"Clé manquante dans la réponse API : {e}")
        return None






# crypto_symbol = 'PRE'
# price = get_crypto_price(crypto_symbol)

# if price is not None:
#     print(f"Le prix actuel de {crypto_symbol} est {price:.8f} USD")
# else:
#     print("Impossible de récupérer le prix. Une erreur s'est produite.")


