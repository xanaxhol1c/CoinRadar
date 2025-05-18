from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  

    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),  
            'password': attrs.get('password')
        }

        user = authenticate(**credentials)

        if user is None or not user.is_active:
            raise serializers.ValidationError("Invalid email or password")

        refresh = self.get_token(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
