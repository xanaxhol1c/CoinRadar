from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import CustomTokenObtainPairSerializer, RegisterUserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Get email and password of user and tries to login

    This endpoint takes two required arguments: email and password. After that endpoint
    searches for that user in database.
    If user was found, endpoint generates refresh and access tokens for user.
    Otherwise it returns error that user with given data was not found.

    Parameters:
        - email (str): Email of user that he used when registered in app.
        - password (str): Password of user that he used when registered in app.

    Responses:
        - 200 OK: A JSON data with refresh and access tokens.
        - 401 Unauthorized: If user was not found.

    Source:
        - PostgreSQL database
    """
    serializer = CustomTokenObtainPairSerializer()

class RegisterUserView(APIView):
    def post(self, request):
        """
        Get data from user and registers him in database.

        This endpoint takes three required arguments: username, email and password. After that endpoint
        checks are username and email unique.
        If yes, endpoint returns HTTP 201 and message that user was created successfuly.
        Otherwise it returns error HTTP 400 that given data can't be used for registration.

        Parameters:
            - username (str): Username of user for app. Has to be unique.
            - email (str): Email of user for app. Has to be unique.
            - password (str): Password of user for app. Doesn't have to be unique.

        Responses:
            - 201 Created: A message that user was created successfully.
            - 400 Bad Request: If given data can't be used for registration.

        Source:
            - PostgreSQL database
        """
        serializer = RegisterUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message": "User created successfully"}, status=status.HTTP_400_BAD_REQUEST)

