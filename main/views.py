from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Coin
from .serializers import CoinSerializer
import requests

from coinradar.settings import COINGECKO_SECRET

class TopCoinView(APIView):
    def get(self, request):
        limit = int(request.query_params.get('limit', 5))

        if limit > 100:
            return Response({'message': 'limit can`t be greater than 100'}, status=400)

        top_coins = Coin.objects.order_by("-market_cap")[:limit]

        serializer = CoinSerializer(top_coins, many=True)

        return Response(serializer.data)

    
class RefreshCoinsView(APIView):
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
            return

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

        return Response({"message": "Coins refreshed successfully."})
        