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

    class Meta:
        db_table = 'coin'
        ordering = ['-market_cap']
        verbose_name = 'Coin'
        verbose_name_plural = 'Coins'

    def __str__(self):
        return f'{self.name} ({self.ticker})'
