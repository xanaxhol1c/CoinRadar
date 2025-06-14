from django.core.management.base import BaseCommand
import requests
from datetime import datetime
from coins.models import CoinHistory, Coin
import time

class Command(BaseCommand):
    help = 'Update coin history from CoinGecko'

    def handle(self, *args, **options):
        all_coins = Coin.objects.all()

        for coin in all_coins:
            url = f'https://api.coingecko.com/api/v3/coins/{coin.id}/market_chart/range'
            headers = {
                "accept": "application/json"
            }

            params = {
                "vs_currency": "usd",
                "from": 1746931200,  
                "to": 1749878400    
            }

            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()

                if not coin:
                    self.stdout.write(self.style.ERROR(f"Coin with id '{coin.id}' not found"))
                    return

                history_objects = []
                seen_days = set()

                for price, market_cap, volume in zip(
                    data['prices'], data['market_caps'], data['total_volumes']
                ):
                    timestamp = int(price[0]) // 1000
                    date_obj = datetime.fromtimestamp(timestamp).date()

                    if date_obj in seen_days:
                        continue

                    seen_days.add(date_obj)

                    if CoinHistory.objects.filter(coin_id=coin.id, date=date_obj).exists():
                        continue

                    print(date_obj, price[1], market_cap, volume)

                    history_objects.append(CoinHistory(
                        coin_id=coin.id,
                        coin_name=coin.name,
                        coin_ticker=coin.slug,
                        date=date_obj,
                        price=float(price[1]),
                        market_cap=float(market_cap[1]),
                        volume_24h=float(volume[1]),
                        percent_change_24h=0.0
                    ))


                CoinHistory.objects.bulk_create(history_objects)
                time.sleep(60)

            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Request error: {e}"))
        self.stdout.write(self.style.SUCCESS(f"Prepared {len(history_objects)} records"))  
