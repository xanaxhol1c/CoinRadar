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


def refresh_top_coins(response_data):
    Coin.objects.all().delete()

    top_coins = []

    for coin in response_data:
        top_coin = Coin(
            id=coin.get("id"),
            name=coin.get("name"),
            ticker=coin.get("symbol").upper(),
            price=coin.get("current_price"),
            market_cap=coin.get("market_cap"),
            volume_24h=coin.get("total_volume"),
            percent_change_24h=coin.get("price_change_percentage_24h")
        )

        top_coins.append(top_coin)

    Coin.objects.bulk_create(top_coins) 



def save_coin_history(coins_data_list):
    today = date.today()

    history_coins = []

    for coin_data in coins_data_list:
        prev_coin = CoinHistory.objects.filter(coin_id=coin_data.id).order_by('-date').first()

        if prev_coin and prev_coin.price and prev_coin.price != 0:
            try:
                percent_change_24h = Decimal(((coin_data.price - prev_coin.price) / prev_coin.price)) * 100
                percent_change_24h = percent_change_24h.quantize(Decimal(0.01), rounding=ROUND_HALF_UP)
                
            except (InvalidOperation, TypeError, ValueError) as e:
                percent_change_24h = Decimal("0.00")  
        
        else: 
            percent_change_24h = coin_data.percent_change_24h

        history = CoinHistory(  
            coin_id=coin_data.id,
            coin_name=coin_data.name,
            coin_ticker=coin_data.ticker,  
            date=today,
            price = coin_data.price,
            market_cap = coin_data.market_cap,
            volume_24h = coin_data.volume_24h,
            percent_change_24h = percent_change_24h
        )

        history_coins.append(history)
  
    CoinHistory.objects.bulk_create(history_coins)
