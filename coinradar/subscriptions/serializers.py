from rest_framework import serializers
from .models import CoinSubscription
from coins.models import Coin
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

class CoinSubscriptionSerializer(serializers.ModelSerializer):
    coin_name = serializers.CharField(source='coin.name', read_only=True)
    coin_ticker = serializers.CharField(source='coin.slug', read_only=True)
    coin_image = serializers.CharField(source='coin.image', read_only=True)
    coin_percent_change_24h = serializers.CharField(source='coin.percent_change_24h', read_only=True)
    
    class Meta:
        model = CoinSubscription
        fields = ['coin_name', 
                  'coin_ticker', 
                  'coin_image', 
                  'threshold_percent', 
                  'coin_percent_change_24h', 
                  'created_at', 
                  'last_notified']


class SubscripeToCoinSerializer(serializers.ModelSerializer):
    coin_slug = serializers.CharField(write_only=True)

    class Meta:
        model = CoinSubscription
        fields = ['coin_slug', 'created_at', 'threshold_percent']

    def validate_coin_slug(self, value):
        try:
            coin = Coin.objects.get(slug=value)
        except Coin.DoesNotExist:
            raise serializers.ValidationError("Coin with given id does not exist")
        return value
    
    def validate(self, attrs):
        user = self.context['request'].user

        coin_slug = attrs.get('coin_slug')

        coin = Coin.objects.filter(slug=coin_slug).first()

        if CoinSubscription.objects.filter(user=user, coin=coin).exists():
            raise serializers.ValidationError("Subscription already exists")

        raw_threshold_percent = attrs.get('threshold_percent')

        if raw_threshold_percent is None:
            raw_threshold_percent = '5.00'

        try:
            threshold_percent = Decimal(str(raw_threshold_percent)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
        except InvalidOperation:
            raise serializers.ValidationError("Wrong threshold percent")

        if threshold_percent < Decimal('5.00'):
            raise serializers.ValidationError("Threshold percent must be >= 5.00%")
        
        attrs['threshold_percent'] = threshold_percent

        return attrs
    
    def create(self, validated_data):
        user = self.context['request'].user
        coin_slug = validated_data['coin_slug']
        coin = Coin.objects.get(slug=coin_slug)
        threshold_percent = validated_data['threshold_percent']

        return CoinSubscription.objects.create(user=user, coin=coin, threshold_percent=threshold_percent)
    
    def update(self, instance, validated_data):
        raw_threshold_percent = validated_data['threshold_percent']

        if raw_threshold_percent is None:
            raw_threshold_percent = '5.00'

        try:
            threshold_percent = Decimal(str(raw_threshold_percent)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
        except InvalidOperation:
            raise serializers.ValidationError("Wrong threshold percent")

        if threshold_percent < Decimal('5.00'):
            raise serializers.ValidationError("Threshold percent must be >= 5.00%")
        
        instance.threshold_percent = threshold_percent

        instance.save()

        return instance

