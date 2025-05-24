from users.models import User
from datetime import timedelta, datetime
from .models import CoinSubscription
from django.utils import timezone
from django.core.mail import send_mail
from django.db.models import Q

from django.conf import settings

def get_users_to_notify(coin):
    six_hours_ago = timezone.now() - timedelta(6)
    threshold_percent = abs(coin.percent_change_24h)


    users_to_notify = CoinSubscription.objects.filter(
        coin = coin,
        threshold_percent__lte = threshold_percent
        ).filter(
            Q(last_notified__lte = six_hours_ago) | Q(last_notified__isnull = True)
            )
        
    return users_to_notify

def send_price_notification(user, coin):
    user_email = user.email

    subject = "📈 CoinRadar Price Notification!"

    message = (
        f"Dear {user.username},\n\n"
        f"The price of {coin.name} has changed by {coin.percent_change_24h:.2f}% in the last 24 hours.\n"
        f"Check your CoinRadar dashboard to stay updated.\n\n"
        f"Best regards,\n"
        f"The CoinRadar Team"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False
    )

