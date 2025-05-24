from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Coin, CoinHistory
from .serializers import CoinSerializer, CoinHistorySerializer
# from .utils import save_coin_history
from datetime import date, timedelta, datetime

import requests

from coinradar.settings import COINGECKO_SECRET

class CoinListView(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        top_coins = Coin.objects.order_by("-market_cap")

        serializer = CoinSerializer(top_coins, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TopCoinView(APIView):
    permission_classes = [IsAuthenticated]

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
            history_date = date.today() - timedelta(days=int(days))

            coin_history = coin_history.filter(date__gte=history_date)
      
        elif start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

            end_date = datetime.strptime(end_date, "%Y-%m-%d").date() + timedelta(days=1)

            coin_history = coin_history.filter(date__gte=start_date, date__lt=end_date)

        if not coin_history.exists():
            return Response({"message": "Coin history not found"})

        serializer = CoinHistorySerializer(coin_history.order_by('-date'), many=True)

        return Response(serializer.data)
        

        
        



# class RefreshCoinsView(APIView):
#     permission_classes = [IsAdminUser]
#     def post(self, request):
#         coingeko_request_url = "https://api.coingecko.com/api/v3/coins/markets"

#         headers = {
#             "accept": "application/json",
#             "x-cg-demo-api-key": COINGECKO_SECRET
#         }

#         params = {
#             "vs_currency": "usd",
#             "per_page": 100,
#             "page": 1
#         }

#         try:
#             coingeko_response = requests.get(coingeko_request_url, headers=headers, params=params)
#             coingeko_response.raise_for_status()
#             response_data = coingeko_response.json()

#         except requests.RequestException as e:
#             print(f"Error fetching data: {e}")
#             return Response({"message": f"Error fetching data: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # for coin in response_data:
        #     Coin.objects.update_or_create(
        #         id=coin.get("id"),
        #         defaults={
        #             "name": coin.get("name"),
        #             "ticker": coin.get("symbol").upper(),
        #             "price": coin.get("current_price"),
        #             "market_cap": coin.get("market_cap"),
        #             "volume_24h": coin.get("total_volume"),
        #             "percent_change_24h": coin.get("price_change_percentage_24h")
        #         }
        #     )

        # save_coin_history(response_data)

        # return Response({"message": "Coins refreshed successfully."}, status=status.HTTP_200_OK)