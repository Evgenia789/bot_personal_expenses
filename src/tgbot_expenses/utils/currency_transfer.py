import aiohttp
from bs4 import BeautifulSoup


async def get_currency_rate(currencies: str) -> float:
    """
    Get the exchange rate for a currency pair.

    Args:
        currencies: A string representing the currency pair,
                    in the format "CURRENCY1 to CURRENCY2".

    Returns:
        A float representing the current exchange rate for
        the specified currency pair.

    Raises:
        ValueError: If the specified currency pair is invalid
                    or not found on the website.

    """
    async with aiohttp.ClientSession() as session:
        headers = {'User-Agent': ('Mozilla/5.0 (Macintosh; '
                                  'Intel Mac OS X 10_15_3) '
                                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/80.0.3987.149 Safari/537.36')}

        url = f"https://www.google.com/search?q={currencies}"
        async with session.get(url, headers=headers) as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            rate = soup.select_one('span[class="DFlfde SwHCTb"]')
            if rate is None:
                raise ValueError(f"Exchange rate not found for currency pair {currencies}")
            rate = rate.text
            return float(rate.replace(",", "."))
