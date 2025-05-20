from django.urls import path
from .views import CoinListView, TopCoinView, CoinDetailView, CoinHistoryView

urlpatterns = [
    path('', CoinListView.as_view(), name='coins-list'),
    path('top/', TopCoinView.as_view(), name='top-coins'),
    path('<slug:coin_slug>/', CoinDetailView.as_view(), name='coin-details'),
    path('<slug:coin_slug>/history', CoinHistoryView.as_view(), name='coin-history')
]