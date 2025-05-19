from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Coin
from .serializers import CoinSerializer
import requests

from coinradar.settings import COINGECKO_SECRET

class TopCoinView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        limit = int(request.query_params.get('limit', 5))

        if limit > 100 or limit <= 0:
            return Response({'message': 'limit must be between 1 and 100'}, status=status.HTTP_400_BAD_REQUEST)

        top_coins = Coin.objects.order_by("-market_cap")[:limit]

        serializer = CoinSerializer(top_coins, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    
class RefreshCoinsView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        coingeko_request_url = "https://api.coingecko.com/api/v3/coins/markets"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": COINGECKO_SECRET
        }

        params = {
            "vs_currency": "usd",
            "per_page": 100,
            "page": 1
        }

        try:
            coingeko_response = requests.get(coingeko_request_url, headers=headers, params=params)
            coingeko_response.raise_for_status()
            response_data = coingeko_response.json()

        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return Response({"message": f"Error fetching data: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        for coin in response_data:
            Coin.objects.update_or_create(
                id=coin.get("id"),
                defaults={
                    "name": coin.get("name"),
                    "ticker": coin.get("symbol").upper(),
                    "price": coin.get("current_price"),
                    "market_cap": coin.get("market_cap"),
                    "volume_24h": coin.get("total_volume"),
                    "percent_change_24h": coin.get("price_change_percentage_24h")
                }
            )

        return Response({"message": "Coins refreshed successfully."}, status=status.HTTP_200_OK)