from django.db import models
from users.models import User
from coins.models import Coin

class CoinSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    threshold_percent = models.DecimalField(max_digits=6, decimal_places=2, default=5.0)
    last_notified = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'coin_subscription'
        unique_together = ('user', 'coin')
        verbose_name = 'Coin Subscription'
        verbose_name_plural = 'Coin Subscriptions'

    def __str__(self):
        return f'{self.user.username} subscribed to {self.coin.name} with threshold >= {self.threshold_percent}%'