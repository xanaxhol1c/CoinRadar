from django.urls import path
from .views import TopCoinView, RefreshCoinsView

urlpatterns = [
    path('top/', TopCoinView.as_view(), name='top-coins'),
    path('top/refresh/', RefreshCoinsView.as_view(), name='refresh-coins')
]