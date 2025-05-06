from django.utils import timezone

from currencies.models import Currency, CurrencyPrice, CurrencyType
from finance_tracker.scripts.get_coingecko_currencies import (
    fetch_top_cryptos,
    fetch_top_fiats,
)


def update_active_currencies():
    """
    Update the current price of every active fiat currency in the database (in a Currency model).
    Also save the current price with data in the database (in a CurrencyPrice model).
    """
    update_fiat_currencies()
    update_crypto_currencies()


def update_fiat_currencies():
    currencies = Currency.objects.filter(type=CurrencyType.FIAT, is_active=True)
    if not currencies.exists():
        print("No active fiat currency found. Skipping update.")
        return

    prices = fetch_top_fiats()
    price_map = {item["code"].lower(): item for item in prices}
    today = timezone.now().date()

    for currency in currencies:
        data = price_map.get(currency.id)
        if not data:
            print(f"Price for fiat '{currency.id}' not found.")
            continue

        rate = data["price_usd"]
        if not rate:
            print(f"Price for fiat '{currency.id}' not found, skipping update.")
            continue

        currency.current_price = rate
        currency.save(update_fields=["current_price"])

        if not CurrencyPrice.objects.filter(currency=currency, date=today).exists():
            CurrencyPrice.objects.create(
                currency=currency,
                date=today,
                price=rate,
            )


def update_crypto_currencies():
    currencies = Currency.objects.filter(type=CurrencyType.CRYPTO, is_active=True)
    if not currencies.exists():
        print("No active crypto currency found. Skipping update.")
        return

    per_page = 200
    pages = -(-currencies.count() // per_page)
    today = timezone.now().date()

    for page in range(1, pages + 1):
        page_counter = f"page {page}/{pages}"

        prices = fetch_top_cryptos(
            page=page, per_page=per_page, coin_ids=[c.id for c in currencies]
        )
        if not prices:
            print(f"No data found for {page_counter}.")
            continue

        for token_data in prices:
            rate = token_data["price_usd"]
            if not rate:
                print(
                    f"Price for crypto '{token_data['id']}' not found, skipping update."
                )
                continue

            currency = currencies.get(id=token_data["id"])
            currency.current_price = rate
            currency.save(update_fields=["current_price"])

            if not CurrencyPrice.objects.filter(currency=currency, date=today).exists():
                CurrencyPrice.objects.create(currency=currency, date=today, price=rate)
