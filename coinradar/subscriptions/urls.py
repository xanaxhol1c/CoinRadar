from django.urls import path
from .views import CoinSubscriptionView

urlpatterns = [
    path('', CoinSubscriptionView.as_view(), name="create_subscription"),
    path('<slug:coin_slug>/', CoinSubscriptionView.as_view(), name="get_subscription_by_slug")
]
