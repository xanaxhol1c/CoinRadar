from celery import shared_task
from .utils import get_users_to_notify, send_price_notification
from datetime import datetime

@shared_task
def check_and_notify_users():
    from coins.models import Coin

    for coin in Coin.objects.all():
        if abs(coin.price_change_24h or 0) < 5:
            continue
        
        subscribed_users = get_users_to_notify(coin)

        for sub in subscribed_users:
            send_price_notification(sub.user, coin)
            sub.last_notified = datetime.now()
            sub.save(update_fields=['last_notified'])


