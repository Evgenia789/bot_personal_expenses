from src.tgbot_expenses.utils.currency_transfer import get_currency_rate


async def get_dollar_amount(bill: str, amount: float) -> float:
    """
    Converts the given amount of a specified currency to its equivalent
    in US dollars.

    :param bill: A string that represents the currency of the given amount.
    :type bill: str
    :param amount: A float that represents the amount of the given currency
                   to convert.
    :type amount: float
    :return: float
    """
    currencies = f'USD to {bill.split(" ")[-1]}'
    currency_rate = 1 \
        if currencies == "USD to USD" \
        else await get_currency_rate(currencies=currencies)

    return round(amount / currency_rate, 2)
