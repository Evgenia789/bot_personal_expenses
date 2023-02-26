from src.tgbot_expenses.utils.currency_transfer_from_usd import \
    get_currency_rate


async def get_new_amount_currency(bill: str, dollar_amount: float) -> float:
    """Get a new amount in the currency"""
    currency = bill.split(" ")[-1]
    currency_rate = get_currency_rate(currency=currency)

    return round(dollar_amount * currency_rate, 2)
