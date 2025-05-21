from django.db import models
from users.models import User
from coins.models import Coin

class CoinSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'coin_subscription'
        unique_together = ('user', 'coin')