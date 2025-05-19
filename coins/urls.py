from django.urls import path
from .views import TopCoinView, RefreshCoinsView

urlpatterns = [
    path('top/', TopCoinView.as_view(), name='top-coins'),
    path('refresh/', RefreshCoinsView.as_view(), name='refresh-coins')
]