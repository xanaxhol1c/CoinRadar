from users.models import User
from datetime import timedelta, datetime
from .models import CoinSubscription
from django.core.mail import EmailMessage



def get_users_to_notify(coin):
    users_to_notify = CoinSubscription.objects.filter(
        coin = coin,
        threshold_percent__lte = abs(coin.percent_change_24h),
        last_notified__lte = datetime.now() - timedelta(6)
    )

    return users_to_notify

def send_price_notification(user, coin):
    user_email = user.email

    email = EmailMessage(
            subject=f"CoinRadar Price Notification!",
            message = (
                f"Dear {user.username},\n\n"
                f"The price of {coin.name} changed by {coin.percent_change_24h:.2f}% in the last 24 hours.\n"
                f"You can check the latest price in your CoinRadar account.\n\n"
                f"Best regards,\nCoinRadar Team"
            )
        )
    
    email.send(fail_silently=True)
