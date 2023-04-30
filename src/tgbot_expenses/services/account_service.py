import logging
from decimal import Decimal

from sqlalchemy.sql import select

from src.tgbot_expenses.database.db import AsyncSessionWithEnter, database
from src.tgbot_expenses.models.expense_tracking_models import Account


async def insert_account(account_name: str, account_amount: Decimal,
                         telegram_id: int) -> None:
    """
    Insert a new entry into the 'accounts' table with the given account
    name, account amount and telegram_id.
    :param account_name: The name of the account to insert.
    :type account_name: str
    :param account_amount: The amount associated with the account
                           to insert.
    :type account_amount: Decimal
    :param telegram_id: The user's Telegram ID.
    :type telegram_id: int
    :return: None
    """
    async with AsyncSessionWithEnter(database.engine) as session:
        account = Account(name=account_name, balance=account_amount,
                          user_id=telegram_id)
        session.add(account)
        await session.commit()


async def get_amount(account_id: int, telegram_id: int) -> Decimal:
    """
    Retrieve the amount associated with the given account ID from
    the 'accounts' table and the given telegram ID from the 'users'
    table.
    :param account_id: The ID of the account to retrieve the amount for.
    :type account_id: int
    :param telegram_id: The user's Telegram ID.
    :type telegram_id: int
    :return: The balance associated with the account.
    """
    async with AsyncSessionWithEnter(database.engine) as session:
        balance_obj = await session.execute(select(Account.balance).where(
            Account.user_id == telegram_id, Account.id == account_id
        ))
        balance = balance_obj.scalars().first()

        return balance


async def get_all_accounts(telegram_id: int) -> str:
    """
    Retrieve the names of all active accounts from the 'accounts' table.
    :param telegram_id: The user's Telegram ID.
    :type telegram_id: int
    :return: A string containing the names of all active accounts,
             separated by semicolons.
    """
    async with AsyncSessionWithEnter(database.engine) as session:
        accounts = await session.execute(select(Account.name).where(
            Account.user_id == telegram_id, Account.account_status == "active"
        ))

        return ";".join([account[0] for account in accounts])


async def update_amount(account_from: str,
                        amount_old_currency: Decimal,
                        currency_amount: Decimal, account_to: str,
                        telegram_id: int) -> None:
    """
    Update the amount for the specified account in the 'accounts' table.
    :param account_from: The name of the account to subtract the old
                         amount from.
    :type account_from: str
    :param amount_old_currency: The old amount in the original currency to
                                subtract from the 'account_from'.
    :type amount_old_currency: Decimal
    :param currency_amount: The amount in the new currency to add
                            to the 'account_to'.
    :type currency_amount: Decimal
    :param account_to: The name of the account to add the new amount to.
    :type account_to: str
    :param telegram_id: The user's Telegram ID.
    :type telegram_id: int
    :return: None
    """
    async with AsyncSessionWithEnter(database.engine) as session:
        async with session.begin():
            try:
                account_obj_from = await session.execute(
                    select(Account).where(
                        Account.user_id == telegram_id,
                        Account.name == account_from
                    ).with_for_update()
                )
                account_obj_to = await session.execute(
                    select(Account).where(
                        Account.user_id == telegram_id,
                        Account.name == account_to
                    ).with_for_update()
                )

                account_from = account_obj_from.scalars().first()
                account_to = account_obj_to.scalars().first()
                account_from.balance -= amount_old_currency
                account_to.balance += currency_amount
                await session.flush()
                await session.commit()
            except AttributeError as e:
                error_message = f"Error: {str(e)}. Account does not exist."
                logging.error(error_message)
                raise ValueError(error_message)


async def archive_account(account_name: str, telegram_id: int) -> None:
    """
    Update the status of the specified account to 'archive'
    in the 'accounts' table.
    :param account_name: The name of the account to be archived.
    :type account_name: str
    :param telegram_id: The user's Telegram ID.
    :type telegram_id: int
    :return: None
    """
    async with AsyncSessionWithEnter(database.engine) as session:
        account_obj = await session.execute(select(Account).where(
            Account.user_id == telegram_id, Account.name == account_name
        ))
        account = account_obj.scalars().first()
        account.account_status = "archive"
        await session.commit()
