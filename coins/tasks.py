from celery import shared_task
from .models import Coin
from .utils import save_coin_history, fetch_data_from_api

@shared_task
def refresh_top_coins_task():
    response_data = fetch_data_from_api()

    for coin in response_data:
        Coin.objects.update_or_create(
            id=coin.get("id"),
            defaults={
                "name": coin.get("name"),
                "ticker": coin.get("symbol").upper(),
                "price": coin.get("current_price"),
                "market_cap": coin.get("market_cap"),
                "volume_24h": coin.get("total_volume"),
                "percent_change_24h": coin.get("price_change_percentage_24h")
            }
        )

    return "Coins refreshed successfully."



@shared_task
def save_coin_history_task():
    data = Coin.objects.all()

    save_coin_history(data)
    return "Coins history saved successfully."