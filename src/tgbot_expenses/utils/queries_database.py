import asyncio
import logging

from src.tgbot_expenses.services.account_service import get_all_accounts
from src.tgbot_expenses.services.category_service import get_all_categories


async def get_all_accounts_with_retry(max_retries: int = 3,
                                      retry_delay: int = 60) -> str:
    """
    Attempt to retrieve all accounts with retries.

    :param max_retries: The maximum number of retries to attempt.
                        Defaults to 3.
    :param retry_delay: The delay in seconds between each retry.
                        Defaults to 60.

    :return: A string containing the names of all accounts.

    :raise: If the maximum number of retries is exceeded,
            an error will be raised.
    """
    for i in range(max_retries):
        try:
            accounts = await get_all_accounts()
            return accounts
        except Exception as e:
            logging.error(f"Error getting accounts: {e}")
            if i < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                raise


async def get_all_categories_with_retry(max_retries: int = 3,
                                        retry_delay: int = 60) -> str:
    """
    Attempt to retrieve all categories with retries.

    :param max_retries: The maximum number of retries to attempt.
                        Defaults to 3.
    :param retry_delay: The delay in seconds between each retry.
                        Defaults to 60.

    :return: A string containing the names of all categories.

    :raise: If the maximum number of retries is exceeded,
            an error will be raised.
    """
    for i in range(max_retries):
        try:
            categories = await get_all_categories()
            return categories
        except Exception as e:
            logging.error(f"Error getting accounts: {e}")
            if i < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                raise
