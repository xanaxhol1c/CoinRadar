from datetime import date
from .models import Coin, CoinHistory
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation, getcontext
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
    for coin in response_data:
        Coin.objects.update_or_create(
            id=coin.get("id"),
            defaults={
            "name": coin.get("name"),
            "ticker": coin.get("symbol").upper(),
            "price": coin.get("current_price"),
            "market_cap": coin.get("market_cap"),
            "volume_24h": coin.get("total_volume"),
            "percent_change_24h": coin.get("price_change_percentage_24h")}
        )



def save_coin_history(coins_data_list):
    history_coins = []

    for coin_data in coins_data_list:
        prev_coin = CoinHistory.objects.filter(coin_id=coin_data.id).order_by('-date').first()

        if prev_coin and prev_coin.price and prev_coin.price != 0:
            
            current_price = Decimal(str(coin_data.price or "0.00"))
            prev_price = Decimal(str(prev_coin.price or "0.00"))

            raw_change = ((current_price - prev_price) / prev_price) * 100
            
            percent_change_24h = raw_change.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                
            # except (InvalidOperation, TypeError, ValueError) as e:
            #     percent_change_24h = Decimal("0.00")  
        
        else: 
            percent_change_24h = coin_data.percent_change_24h

        history = CoinHistory(  
            coin_id=coin_data.id,
            coin_name=coin_data.name,
            coin_ticker=coin_data.slug,  
            date=coin_data.last_updated,
            price = coin_data.price,
            market_cap = coin_data.market_cap,
            volume_24h = coin_data.volume_24h,
            percent_change_24h = percent_change_24h
        )

        history_coins.append(history)
  
    for history in history_coins:
        CoinHistory.objects.get_or_create(
            coin_id=history.coin_id,
            date=history.date,
            defaults={
                "coin_name" : history.coin_name,
                "coin_ticker" : history.coin_ticker,  
                "price" : history.price,
                "market_cap" : history.market_cap,
                "volume_24h" : history.volume_24h,
                "percent_change_24h" : history.percent_change_24h
            })
