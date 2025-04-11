import aiohttp
import asyncio




async def getDataWithAPI(urlAPI : str ,headers : dict, params : dict, nbRetry : int = 2, delayBeforeRetry : int = 10, nameAPI : str = "API service") -> str:
    """
    Asynchronous function to fetch data from an API with retry logic.
    Args:
        urlAPI (str): The URL of the API endpoint to send the GET request to.
        headers (dict): A dictionary of HTTP headers to include in the request.
        params (dict): A dictionary of query parameters to include in the request.
        nbRetry (int, optional): The number of retry attempts in case of failure. Defaults to 2.
        delayBeforeRetry (int, optional): The delay in seconds before retrying a failed request. Defaults to 10.
        nameAPI (str, optional): A name or description of the API service for logging purposes. Defaults to "API service".
    Returns:
        str: The JSON response from the API as a string if the request is successful.
        None: If all retry attempts fail.
    Raises:
        aiohttp.ClientError: For network-related errors during the request.
        Exception: For any other unexpected errors.
    """

    for attempt in range(nbRetry):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=urlAPI,params=params,headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
        
                    print(f"Error: Received HTTP {response.status} from {nameAPI}I")
                    
        except aiohttp.ClientError as e:
            print(f"Network error on attempt {attempt + 1}: {e}")
                
        except Exception as e:
            print(f"Unexpected error on attempt {attempt + 1}: {e}")
        

        print(f"Retrying in {delayBeforeRetry} seconds...")
        asyncio.sleep(delayBeforeRetry)    

    return None
