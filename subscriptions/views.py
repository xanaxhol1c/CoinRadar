from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework import status
from .serializers import SubscripeToCoinSerializer, CoinSubscriptionSerializer
from .models import CoinSubscription
from coins.models import Coin


class CoinSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, coin_slug=None):
        user = request.user
        
        if coin_slug:
            coin = Coin.objects.filter(slug=coin_slug).first()

            if not coin:
                return Response({'message' : 'Coin not found.'}, status=status.HTTP_404_NOT_FOUND)
            
            subscription = CoinSubscription.objects.filter(user=user, coin=coin).first()

            if not subscription:
                return Response({'message' : 'Subscription not found.'}, status=status.HTTP_404_NOT_FOUND)

            serializer = CoinSubscriptionSerializer(subscription)

        else:
            try: 
                subscriptions = CoinSubscription.objects.filter(user=user)
            except CoinSubscription.DoesNotExist:
                return Response({'message' : 'No subscriptions found.'}, status=status.HTTP_404_NOT_FOUND)

            serializer = CoinSubscriptionSerializer(subscriptions, many=True)

        return Response(serializer.data)


    def post(self, request):
        serializer = SubscripeToCoinSerializer(data=request.data, context={'request' : request})
        serializer.is_valid(raise_exception=True)
        subscription = serializer.save()
        
        return Response({'message' : 'Subscribed successfully', 'coin' : subscription.coin.name}, status=status.HTTP_201_CREATED)
    

    def patch(self, request, coin_slug):
        user = request.user

        coin = Coin.objects.filter(slug=coin_slug).first()

        subscription = CoinSubscription.objects.filter(user=user, coin=coin).first()

        if not subscription:
            return Response({'message' : 'Subscription not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SubscripeToCoinSerializer(subscription, data=request.data, partial=True, context = {"request" : request})

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({'message': 'Subscription updated successfully'}, status=status.HTTP_200_OK)    

        
    def delete(self, request, coin_slug):
        user = request.user

        coin = Coin.objects.filter(slug=coin_slug).first()

        if not coin:
            return Response({'message' : 'Coin not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        subscription = CoinSubscription.objects.filter(user=user, coin=coin).first()

        if not subscription:
            return Response({'message' : 'Subscription not found.'}, status=status.HTTP_404_NOT_FOUND)

        subscription.delete()

        return Response({'message' : 'Subscription deleted sucessfully.'}, status=status.HTTP_204_NO_CONTENT)







