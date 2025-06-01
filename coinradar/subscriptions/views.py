from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework import status
from .serializers import SubscripeToCoinSerializer, CoinSubscriptionSerializer
from .models import CoinSubscription
from coins.models import Coin


class CoinSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve all existing coin subscriptions for the authenticated user.

        If JWT Access Token was provided returns all subscriptions for user or
        404 HTTP if no subscriptions of user were found. 

        Authentication:
            Requires a valid JWT Access Token in the Authorization header.

        Returns:
            - 200 OK with subscription(s) data if found.
            - 401 Unauthorized if JWT Acess token was not provided.
            - 404 Not Found if the coin subscriptions were not found.
        
        Source:
            - PostgreSQL database
        """
        user = request.user

        try: 
            subscriptions = CoinSubscription.objects.filter(user=user)
        except CoinSubscription.DoesNotExist:
            return Response({'message' : 'No subscriptions found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CoinSubscriptionSerializer(subscriptions, many=True)

        return Response(serializer.data)


class CoinSubscriptionWithSlug(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, coin_slug=None):
        """
        Retrieve coin subscription by slug for the authenticated user.

        If coin_slug is provided, returns the user's subscription to the specific coin.
        Otherwise, returns an error that coin slug was not provided or searched subscription was not found.

        Authentication:
            Requires a valid JWT Access Token in the Authorization header.

        Parameters:
            - coin_slug (str): The slug identifier of the coin.

        Returns:
            - 200 OK with subscription(s) data if found.
            - 401 Unauthorized if JWT Acess token was not provided.
            - 404 Not Found if the coin or subscription does not exist.
        
        Source:
            - PostgreSQL database
        """
        user = request.user
        
        if coin_slug:
            coin = Coin.objects.filter(slug=coin_slug).first()

            if not coin:
                return Response({'message' : 'Coin not found.'}, status=status.HTTP_404_NOT_FOUND)
            
            subscription = CoinSubscription.objects.filter(user=user, coin=coin).first()

            if not subscription:
                return Response({'message' : 'Subscription not found.'}, status=status.HTTP_404_NOT_FOUND)

            serializer = CoinSubscriptionSerializer(subscription)

            return Response(serializer.data)
        
        return Response({'message' : 'Coin slug is required field'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, coin_slug=None):
        """
        Сreates coin subscription for the authenticated user.

        If coin_slug is provided, creates subscription to the specific coin for user.
        Otherwise, returns an error that either coin doesn't exist or subscription already exists.

        Authentication:
            Requires a valid JWT Access Token in the Authorization header.

        Parameters:
            - coin_slug (str): The slug identifier of the coin to subscribe.

        Returns:
            - 201 Created with subscription(s) data if found.
            - 404 Not Found if the coin with given slug does not exist.
        
        Source:
            - PostgreSQL database
        """
        if not coin_slug:
             return Response({'message' : 'Coin slug is required to create a subscription'}, status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data.copy()
        data['coin_slug'] = coin_slug
        serializer = SubscripeToCoinSerializer(data=data, context={'request' : request})
        serializer.is_valid(raise_exception=True)
        subscription = serializer.save()
        
        return Response({'message' : 'Subscribed successfully', 'coin' : subscription.coin.name}, status=status.HTTP_201_CREATED)

    def patch(self, request, coin_slug):
        """
        Updates threshold percent of coin subscription for the authenticated user.

        If coin_slug is provided, updates subscription to the specific coin for user.
        Otherwise, returns an error that either coin doesn't exist or subscription already exists.

        Authentication:
            Requires a valid JWT Access Token in the Authorization header.

        Parameters:
            - coin_slug (str): The slug identifier of the coin to subscribe.
            - threshold percent(float): New threshold percent for subscription. Has to be >= 5.00

        Returns:
            - 200 OK if subscription updated successfully.
            - 404 Not Found if the coin with given slug does not exist.
        
        Source:
            - PostgreSQL database
        """
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
        """
        Delete coin subscription for the authenticated user.

        If coin_slug is provided, deletes subscription to the specific coin for user.
        Otherwise, returns an error that either coin not found or subscription not found.

        Authentication:
            Requires a valid JWT Access Token in the Authorization header.

        Parameters:
            - coin_slug (str): The slug identifier of the coin to subscribe.

        Returns:
            - 200 OK if subscription updated successfully.
            - 404 Not Found if the coin with given slug does not exist.
        
        Source:
            - PostgreSQL database
        """
        user = request.user

        coin = Coin.objects.filter(slug=coin_slug).first()

        if not coin:
            return Response({'message' : 'Coin not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        subscription = CoinSubscription.objects.filter(user=user, coin=coin).first()

        if not subscription:
            return Response({'message' : 'Subscription not found.'}, status=status.HTTP_404_NOT_FOUND)

        subscription.delete()

        return Response({'message' : 'Subscription deleted sucessfully.'}, status=status.HTTP_204_NO_CONTENT)





