from django.conf import settings
from pycoingecko import CoinGeckoAPI

coingecko_client = CoinGeckoAPI(demo_api_key=settings.COINGECKO_API_KEY)
