from django.db import models
from autoslug import AutoSlugField

class Coin(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    ticker = models.CharField(max_length=15)
    slug = AutoSlugField(populate_from='ticker')
    price = models.DecimalField(max_digits=20, decimal_places=10)
    market_cap = models.DecimalField(max_digits=30, decimal_places=2)
    volume_24h = models.DecimalField(max_digits=30, decimal_places=2)
    percent_change_24h = models.DecimalField(max_digits=6, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)
    image = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'coin'
        ordering = ['-market_cap']
        verbose_name = 'Coin'
        verbose_name_plural = 'Coins'

    def str(self):
        return f'{self.name} ({self.ticker})'
    
class CoinHistory(models.Model):
    coin_id = models.CharField(max_length=50)
    coin_name = models.CharField(max_length=50)
    coin_ticker = models.CharField(max_length=15)
    date = models.DateTimeField(blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    market_cap = models.DecimalField(max_digits=30, decimal_places=2)
    volume_24h = models.DecimalField(max_digits=30, decimal_places=2)
    percent_change_24h = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        db_table = 'coin_history'
        unique_together = ('coin_id', 'date')
        ordering = ['-date']
        verbose_name = 'Coins History'