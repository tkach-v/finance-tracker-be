from currencies.constants import FIAT_CURRENCY_SYMBOLS
from integrations.coingecko.cg_client import coingecko_client


def fetch_top_cryptos(
    vs_currency: str = "usd",
    per_page: int = 200,
    page: int = 1,
    coin_ids: list[str] | None = None,
) -> list[dict[str, any]]:
    """
    Returns a list of cryptocurrencies from CoinGecko:
    - if coin_ids is provided, only for those;
    - otherwise, the top `per_page` by market capitalization.
    """

    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": page,
    }
    if coin_ids:
        params["ids"] = ",".join(coin_ids)

    data = coingecko_client.get_coins_markets(**params)
    result = []
    for item in data:
        result.append(
            {
                "id": item["id"],
                "symbol": item["symbol"].upper(),
                "name": item["name"],
                "price_usd": item["current_price"],
            }
        )
    return result


def fetch_top_fiats(
    limit: int = 200,
    vs_base: str = "usd",
):
    """
    Returns a list of fiat currencies and their exchange rate in USD from CoinGecko.
    """

    codes = coingecko_client.get_supported_vs_currencies()[:limit]
    rates = coingecko_client.get_exchange_rates().get("rates", {})
    btc_to_usd = rates.get(vs_base, {}).get("value") or 0.0

    result = []
    for code in codes:
        code_upper = code.upper()
        if code_upper not in FIAT_CURRENCY_SYMBOLS:
            continue

        info = rates.get(code.lower())
        if not info or not btc_to_usd:
            continue

        if info and btc_to_usd:
            price_usd = btc_to_usd / info["value"]
            result.append(
                {
                    "code": code_upper,
                    "symbol": FIAT_CURRENCY_SYMBOLS[code_upper],
                    "price_usd": round(price_usd, 8),
                }
            )
    return result
