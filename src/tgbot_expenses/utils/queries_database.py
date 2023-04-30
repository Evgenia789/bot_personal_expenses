from src.tgbot_expenses.services.account_service import get_all_accounts
from src.tgbot_expenses.services.category_service import get_all_categories
from src.tgbot_expenses.utils.retry_decorator import retry


@retry(max_retries=3, retry_delay=60)
async def get_all_accounts_with_retry(telegram_id: int) -> str:
    """
    Attempt to retrieve all accounts with retries.

    :return: A string containing the names of all accounts.
    """
    accounts = await get_all_accounts(telegram_id=telegram_id)
    return accounts


@retry(max_retries=3, retry_delay=60)
async def get_all_categories_with_retry(telegram_id: int) -> str:
    """
    Attempt to retrieve all categories with retries.

    :return: A string containing the names of all categories.
    """
    categories = await get_all_categories(telegram_id=telegram_id)
    return categories
