from decimal import Decimal

from src.tgbot_expenses.utils.currency_transfer import get_currency_rate


async def get_dollar_amount(account: str, amount: Decimal) -> Decimal:
    """
    Converts the given amount of a specified currency to its equivalent
    in US dollars.

    :param account: A string that represents the currency of the given amount.
    :type account: str
    :param amount: A Decimal that represents the amount of the given currency
                   to convert.
    :type amount: Decimal
    :return: Decimal
    """
    currencies = f'USD to {account.split(" ")[-1]}'
    currency_rate = 1 \
        if currencies == "USD to USD" \
        else await get_currency_rate(currencies=currencies)

    return round(amount / currency_rate, 2)
