from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import CustomTokenObtainPairSerializer, RegisterUserSerializer
from .models import User

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer = CustomTokenObtainPairSerializer()

class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message": "User created successfully"}, status=status.HTTP_400_BAD_REQUEST)

