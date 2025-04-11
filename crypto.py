from typing import Dict
from enum import Enum
import aiohttp
import asyncio
import os

NB_RETRY = 2
DELAY_BEFORE_RETRY = 10
TOKEN_API_COINGECKO = os.getenv("TOKEN_API_COINGECKO")



class TOKEN(Enum):
    NAME_TOKEN = "name",
    SYMBOL_TOKEN = "symbol",        
    PRICE = "current_price",
    P_24H = "price_change_percentage_24h",
    P_7D = "price_change_percentage_7d",
    P_30D = "price_change_percentage_30d",
    UNIX_DATE_LAST_UPDATE = "time"


class COINDATA(Enum):
    ID = "id"
    NAME = "name"
    SYMBOL = "symbol"
    IMAGE = "image"
    CURRENT_PRICE = "current_price"
    MARKET_CAP = "market_cap"
    MARKET_CAP_RANK = "market_cap_rank"
    FULLY_DILUTED_VALUATION = "fully_diluted_valuation"
    TOTAL_VOLUME = "total_volume"
    HIGH_24H = "high_24h"
    LOW_24H = "low_24h"
    PRICE_CHANGE_24H = "price_change_24h"
    PRICE_CHANGE_PERCENTAGE_24H = "price_change_percentage_24h"
    MARKET_CAP_CHANGE_24H = "market_cap_change_24h"
    MARKET_CAP_CHANGE_PERCENTAGE_24H = "market_cap_change_percentage_24h"
    CIRCULATING_SUPPLY = "circulating_supply"
    TOTAL_SUPPLY = "total_supply"
    MAX_SUPPLY = "max_supply"
    ATH = "ath"
    ATH_CHANGE_PERCENTAGE = "ath_change_percentage"
    ATH_DATE = "ath_date"
    ATL = "atl"
    ATL_CHANGE_PERCENTAGE = "atl_change_percentage"
    ATL_DATE = "atl_date"
    ROI = "roi"
    LAST_UPDATED = "last_updated"









def calculRightUSDValue(valueInToken : float, decimalToken :int, priceToken : float) -> float:
    """Compute the right value in usd

    Args:
        valueInToken (float): the value in number of token 
        decimalToken (int): the decimal value 
        priceToken (float): price of one token

    Returns:
        float: the right value in usd
    """
    return valueInToken / (10 ** decimalToken) * priceToken






async def getCoinPrice(contract_address : str) -> dict:
    """TODO not finished
    """
    urlAPI = "https://api.coingecko.com/api/v3/coins/ethereum/contract/"+contract_address

    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": TOKEN_API_COINGECKO
    }
    for attempt in range(NB_RETRY):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(urlAPI, headers=headers) as response:
                    #response = requests.get(urlAPI, headers=headers)
                    if response.status == 200:
                        jsonAnswer = await response.json()
                        jsonDict = jsonAnswer[0]
                        if "id" in jsonDict:
                            return jsonDict["market_data"]
                    print(f"Error: Received HTTP {response.status} from CoinGecko API")
                    
        except aiohttp.ClientError as e:
            print(f"Network error on attempt {attempt + 1}: {e}")
                
        except Exception as e:
            print(f"Unexpected error on attempt {attempt + 1}: {e}")
        

        print(f"Retrying in {DELAY_BEFORE_RETRY} seconds...")
        asyncio.sleep(DELAY_BEFORE_RETRY)    

    return None




async def getERC20TokenPrice(contract_address : str) -> dict:
    """Get the data market from CoinGecko for a ERC20 Token

    Args:
        contract_address (str): the contract address of the ERC20 token

    Returns:
        Tuple:
            - (str): the contract address of the token on the Ethereum network
            - Dict[str, str]: A dictionary containing the following keys:
                - "nameToken" (str): The name of the token.
                - "symbolToken" (str): The symbol of the token.
                - "price" (float): The current price of the token in USD.
                - "pricePercentage24h" (float): The percentage change in price over the last 24 hours.
                - "pricePercentage7D" (float): The percentage change in price over the last 7 days.
                - "pricePercentage30D" (float): The percentage change in price over the last 30 days.
                - "unixDateLastUpdate" (float): The timestamp of the last update in Unix format.
    
    Documentation:
        See the CoinGecko API documentation for more details:
        https://docs.coingecko.com/v3.0.1/reference/coins-contract-address
    """
    urlAPI = "https://api.coingecko.com/api/v3/coins/ethereum/contract/"+contract_address

    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": TOKEN_API_COINGECKO
    }
    for attempt in range(NB_RETRY):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(urlAPI, headers=headers) as response:
                    #response = requests.get(urlAPI, headers=headers)
                    if response.status == 200:
                        jsonText = await response.json()
                        #print("DEBUG reponsse of requests : " + str(response))
                        #print(f"DEBUG : {contract_address} la donnée envoyé par coingecko est " + str(jsonText))
                        if "market_data" in jsonText:
                            dataMarket = jsonText["market_data"]
                            #print('jsonText["platforms"]["ethereum"] = ' + str(jsonText["platforms"]["ethereum"]))
                            return (jsonText["platforms"]["ethereum"].lower(),
                                    {
                                    TOKEN.NAME_TOKEN :  jsonText["name"],
                                    TOKEN.SYMBOL_TOKEN: jsonText["symbol"],        
                                    TOKEN.PRICE: dataMarket["current_price"]["usd"],
                                    TOKEN.P_24H : dataMarket["price_change_percentage_24h"],
                                    TOKEN.P_7D : dataMarket["price_change_percentage_7d"],
                                    TOKEN.P_30D : dataMarket["price_change_percentage_30d"],
                                    TOKEN.UNIX_DATE_LAST_UPDATE.value : time.time()
                                    })
                    print(f"Error: Received HTTP {response.status} from CoinGecko API")
                    
        except aiohttp.ClientError as e:
            print(f"Network error on attempt {attempt + 1}: {e}")
                
        except Exception as e:
            print(f"Unexpected error on attempt {attempt + 1}: {e}")
        

        print(f"Retrying in {DELAY_BEFORE_RETRY} seconds...")
        asyncio.sleep(DELAY_BEFORE_RETRY)    

    return None

