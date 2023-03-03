import asyncio

from src.tgbot_expenses.utils.currency_transfer import get_currency_rate
from src.tgbot_expenses.utils.date_formatting import get_now_date


async def get_message_currency_exchange_rates() -> str:
    """
    Asynchronously fetches the current exchange rates for several currency
    pairs and returns a formatted message with the rates and the current date.

    :return: str
    """
    currency_pairs = ["EUR to RSD", "USD to RSD", "USD to EUR",
                      "USD to RUB", "EUR to RUB"]
    tasks = [get_currency_rate(pair) for pair in currency_pairs]
    results = await asyncio.gather(*tasks)
    now = get_now_date(date_format='%d.%m.%Y %H:%M:%S')
    message = f"Date: {now}\n\n"
    for i, rate in enumerate(results):
        if rate is None:
            message += f"{currency_pairs[i]}: N/A\n"
        else:
            message += f"{currency_pairs[i]}: {rate:.2f}\n"
    return message
