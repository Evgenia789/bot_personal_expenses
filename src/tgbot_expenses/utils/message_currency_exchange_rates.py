from src.tgbot_expenses.utils.currency_transfer import get_currency_rate
from src.tgbot_expenses.utils.date_formatting import get_now_date


async def get_message_currency_exchange_rates() -> str:
    """Get a message about the exchange rate"""
    text_message = f"Date: {get_now_date(date_format='%d.%m.%Y %H:%M:%S')}\n\n"
    for currencies in ["EUR/RSD", "USD/RSD", "USD/EUR", "USD/RUB", "EUR/RUB"]:
        text_message += (f"{currencies}: "
                         f"{get_currency_rate(currencies=currencies)}\n")

    return text_message
