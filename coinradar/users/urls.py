from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterUserView
from users.views import CustomTokenObtainPairView

urlpatterns=[
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]