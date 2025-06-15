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
from redis.exceptions import ConnectionError

import logging

logger = logging.getLogger(__name__)

class CoinListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve a list of coins sorted by market capitalization.

        This endpoint first attempts to fetch the data from the Redis cache using
        a predefined cache key. If the cache is available and contains data, it 
        returns the cached result as a JSON response. If Redis is unavailable or 
        empty, it falls back to querying the PostgreSQL database.

        Returns:
            - 200 OK: A JSON list of coins ordered by market capitalization.
            - 401 Unauthorized: If the user is not authenticated.

        Source:
            - Redis (if available)
            - PostgreSQL (fallback)
        """
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
        """
        Retrieve a list of top N coins sorted by market capitalization.

        This endpoint tries to get top N coins from database. 
        If limit > 100 or limit < 5 then returns HTTP 400 Bad Request. 
        Otherwise fetches top N coins from PostgreSQL database and returns 
        result as a JSON response.

        Params:
            limit: int

        Returns:
            - 200 OK: A JSON list of coins ordered by market capitalization.
            - 400 Bad Request: If limit > 100 or limit < 5 

        Source:
            - PostgreSQL database
        """
        limit = int(request.query_params.get('limit', 5))

        if limit > 100 or limit <= 0:
            return Response({'message': 'limit must be between 1 and 100'}, status=status.HTTP_400_BAD_REQUEST)

        top_coins = Coin.objects.order_by("-market_cap")[:limit]

        serializer = CoinSerializer(top_coins, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class CoinDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, coin_slug):
        """
        Retrieve data of one specific coin by slug(id).

        This endpoint accepts a coin slug and searches for coin with 
        that id in PostgreSQL database. If coin with that id wasn't found 
        returns HTTP 404 Not Found. Otherwise returns JSON data of coin.

        Path Parameters:
            - coin_slug (str): The unique identifier (id) of the coin.

        Returns:
            - 200 OK: A JSON list of coins ordered by market capitalization.
            - 404 Not Found: If coin with that id wasn't found.

        Source:
            - PostgreSQL database
        """
        coin = Coin.objects.filter(id=coin_slug).first()

        if coin is None:
            return Response({"message" : "Coin not found"}, status.HTTP_404_NOT_FOUND)
        
        serializer = CoinSerializer(coin, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

class CoinHistoryView(APIView):
    def get(self, request, coin_slug):
        """
        Retrieve historical data for a specific coin.

        This endpoint returns historical price data for a given coin, identified by its slug(id).
        The user can optionally specify a period using the days parameter or a custom
        date range using start_date and end_date.

        Path Parameters:
            - coin_slug (str): The unique identifier (id) of the coin.

        Query Parameters (optional):
            - days (int): Number of recent days to retrieve data for (e.g., days=7).
            - start_date (str): Start date of the period in YYYY-MM-DD format.
            - end_date (str): End date of the period in YYYY-MM-DD format (inclusive).

            Note: Either days or (start_date and end_date) can be used. If both are omitted,
            history will be returned by days.

        Responses:
            - 200 OK: A JSON list of historical data points for the coin.
            - 404 Not Found: If no coin history was found for the given id or date range.

        Source:
            - PostgreSQL database
        """
        days = request.query_params.get("days")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        coin_history = CoinHistory.objects.filter(coin_id=coin_slug)
        
        if days:
            history_date = timezone.now() - timedelta(days=int(days))

            coin_history = coin_history.filter(date__gt=history_date)
      
        elif start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

            end_date = datetime.strptime(end_date, "%Y-%m-%d").date() + timedelta(days=1)

            coin_history = coin_history.filter(date__gte=start_date, date__lt=end_date)

        if not coin_history.exists():
            return Response({"message": "Coin history not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CoinHistorySerializer(coin_history.order_by('-date'), many=True)

        return Response(serializer.data)
        