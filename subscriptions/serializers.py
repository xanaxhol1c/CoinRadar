from rest_framework import serializers
from .models import CoinSubscription
from coins.models import Coin


class CoinSubscriptionSerializer(serializers.ModelSerializer):
    coin_name = serializers.CharField(source='coin.name', read_only=True)
    coin_ticker = serializers.CharField(source='coin.slug', read_only=True)
    
    class Meta:
        model = CoinSubscription
        fields = ['coin_name', 'coin_ticker', 'created_at']


class SubscripeToCoinSerializer(serializers.ModelSerializer):
    coin_id = serializers.CharField(write_only=True)

    class Meta:
        model = CoinSubscription
        fields = ['coin_id']

    def validate_coin_id(self, value):
        try:
            coin = Coin.objects.get(id=value)
        except Coin.DoesNotExist:
            raise serializers.ValidationError("Coin with given id does not exist")
        return value
    
    def validate(self, attrs):
        user = self.context['request'].user

        coin_id = attrs.get('coin_id')

        if CoinSubscription.objects.filter(user=user, coin_id=coin_id).exists():
            return serializers.ValidationError("Subscription already exists")
        
        return attrs
    
    def create(self, validated_data):
        user = self.context['request'].user
        coin = Coin.objects.get(id=validated_data['coin_id'])

        return CoinSubscription.objects.create(user=user, coin=coin)
