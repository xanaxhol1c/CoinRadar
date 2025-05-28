from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Coin, CoinHistory
from .serializers import CoinSerializer, CoinHistorySerializer
from datetime import timedelta, datetime
from django.utils import timezone
from django.core.cache import cache
from coinradar.settings import TOP_COINS_CACHE_KEY
from django.core.cache.backends.base import InvalidCacheBackendError

import logging

logger = logging.getLogger(__name__)

class CoinListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            top_coins = cache.get(TOP_COINS_CACHE_KEY)

        except (ConnectionError, InvalidCacheBackendError) as e:
            logger.warning(f'Redis connection failed: {e}')
            top_coins = None
            
            
        if top_coins:
            return Response(top_coins)
        
        else:
            top_coins = Coin.objects.order_by("-market_cap")

            serializer = CoinSerializer(top_coins, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)


class TopCoinView(APIView):

    def get(self, request):
        limit = int(request.query_params.get('limit', 5))

        if limit > 100 or limit <= 0:
            return Response({'message': 'limit must be between 1 and 100'}, status=status.HTTP_400_BAD_REQUEST)

        top_coins = Coin.objects.order_by("-market_cap")[:limit]

        serializer = CoinSerializer(top_coins, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class CoinDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, coin_slug):
        
        coin = Coin.objects.filter(slug=coin_slug).first()

        if coin is None:
            return Response({"message" : "Coin not found"}, status.HTTP_200_OK)
        
        serializer = CoinSerializer(coin, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

class CoinHistoryView(APIView):
    def get(self, request, coin_slug):
        days = request.query_params.get("days")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        coin_history = CoinHistory.objects.filter(coin_ticker=coin_slug)
        
        if days:
            history_date = timezone.now() - timedelta(days=int(days))

            coin_history = coin_history.filter(date__gt=history_date)
      
        elif start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

            end_date = datetime.strptime(end_date, "%Y-%m-%d").date() + timedelta(days=1)

            coin_history = coin_history.filter(date__gte=start_date, date__lt=end_date)

        if not coin_history.exists():
            return Response({"message": "Coin history not found"})

        serializer = CoinHistorySerializer(coin_history.order_by('-date'), many=True)

        return Response(serializer.data)
        