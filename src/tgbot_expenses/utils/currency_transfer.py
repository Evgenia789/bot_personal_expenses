from decimal import Decimal

import aiohttp
from bs4 import BeautifulSoup


async def get_currency_rate(currencies: str) -> Decimal:
    """
    Get the exchange rate for a currency pair.

    :param currencies: A string representing the currency pair, in the format
                       "CURRENCY1 to CURRENCY2".
    :type currencies: str
    :return: Decimal
    :raises ValueError: If the specified currency pair is invalid or not found
                        on the website.
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
            return Decimal(rate.replace(",", "."))
