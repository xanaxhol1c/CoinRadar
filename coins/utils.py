from datetime import date
from .models import Coin, CoinHistory
import requests
from coinradar.settings import COINGECKO_SECRET

def fetch_data_from_api():
    coingeko_request_url = "https://api.coingecko.com/api/v3/coins/markets"

    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": COINGECKO_SECRET
    }

    params = {
        "vs_currency": "usd",
        "per_page": 100,
        "page": 1
    }

    try:
        coingeko_response = requests.get(coingeko_request_url, headers=headers, params=params)
        coingeko_response.raise_for_status()
        response_data = coingeko_response.json()
        return response_data

    except requests.RequestException as e:
        return {"message": f"Error fetching data: {e}"}



def save_coin_history(coins_data_list):
    today = date.today()

    history_coins = []

    for coin_data in coins_data_list:
        try:
            coin = Coin.objects.get(id=coin_data.get("id"))
        except:
            continue

        history = CoinHistory(  
            coin=coin,  
            date=today,
            price = coin_data.get("price"),
            market_cap = coin_data.get("market_cap"),
            volume_24h = coin_data.get("volume_24h"),
            percent_change_24h = coin_data.get("percent_change_24h")
        )

        history_coins.append(history)

    CoinHistory.objects.bulk_create(history_coins)
