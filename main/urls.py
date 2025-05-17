from django.urls import path
from .views import TopCoinView, RefreshCoinsView

urlpatterns = [
    path('top-coins/', TopCoinView.as_view(), name='top-coins'),
    path('refresh-coins/', RefreshCoinsView.as_view(), name='refresh-coins')
]
