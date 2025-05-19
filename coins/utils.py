from datetime import date
from .models import Coin, CoinHistory
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
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
        # try:
        #     coin = Coin.objects.get(id=coin_data.get("id"))
        # except:
        #     continue

        prev_coin = CoinHistory.objects.filter(coin=coin_data).order_by('-date').first()

        if prev_coin and prev_coin.price and prev_coin.price != 0:
            try:
                percent_change_24h = Decimal(((coin_data.price - prev_coin.price) / prev_coin.price)) * 100
                percent_change_24h = percent_change_24h.quantize(Decimal(0.01), rounding=ROUND_HALF_UP)
                
            except (InvalidOperation, TypeError, ValueError) as e:
                percent_change_24h = Decimal("0.00")  
        
        else: 
            percent_change_24h = coin_data.percent_change_24h

        history = CoinHistory(  
            coin=coin_data,  
            date=today,
            price = coin_data.price,
            market_cap = coin_data.market_cap,
            volume_24h = coin_data.volume_24h,
            percent_change_24h = percent_change_24h
        )

        history_coins.append(history)
  
    CoinHistory.objects.bulk_create(history_coins)
