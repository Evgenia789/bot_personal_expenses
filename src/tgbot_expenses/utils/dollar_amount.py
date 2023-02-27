from src.tgbot_expenses.utils.currency_transfer import get_currency_rate


async def get_dollar_amount(bill: str, amount: float) -> int:
    """Get dollar amount"""
    currencies = f'USD/{bill.split(" ")[-1]}'
    currency_rate = 1 \
        if currencies == "USD/USD" \
        else get_currency_rate(currencies=currencies)

    return round(amount / currency_rate, 2)
