from src.tgbot_expenses.utils.currency_transfer import get_currency_rate


async def get_dollar_amount(bill: str, amount: float) -> int:
    """Get dollar amount"""
    currency = bill.split(" ")[-1]
    currency_rate = 1 \
        if currency == "USD" \
        else get_currency_rate(currency=currency)

    return round(amount * currency_rate, 2)
