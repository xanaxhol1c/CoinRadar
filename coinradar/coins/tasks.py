from celery import shared_task
from .models import Coin
from .utils import save_coin_history, fetch_data_from_api, refresh_top_coins

@shared_task
def refresh_top_coins_task():
    response_data = fetch_data_from_api()

    refresh_top_coins(response_data)
    return "Coins refreshed successfully."


@shared_task
def save_coin_history_task():
    data = Coin.objects.all()

    save_coin_history(data)
    return "Coins history saved successfully."