from rest_framework.serializers import ModelSerializer
from .models import Coin, CoinHistory

class CoinSerializer(ModelSerializer):
    class Meta:
        model = Coin
        fields = '__all__'

class CoinHistorySerializer(ModelSerializer):
    class Meta:
        model = CoinHistory
        fields = ["coin_id",
                  "coin_name",
                  "coin_ticker",
                  "date",
                  "price",
                  "market_cap",
                  "volume_24h",
                  "percent_change_24h"]