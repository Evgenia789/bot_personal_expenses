from decimal import Decimal

from sqlalchemy.sql import select

from src.tgbot_expenses.database.db import AsyncSessionWithEnter, database
from src.tgbot_expenses.models.expense_tracking_models import Account, Income


async def insert_income(account_name: str, amount: Decimal) -> None:
    """
    Inserts a new income entry into the database for a given account.

    :param account_name: The name of the account for which to insert
                         the income.
    :type account_name: str
    :param amount: The amount of the income to insert.
    :type amount: Decimal
    :return: None
    """
    async with AsyncSessionWithEnter(database.engine) as session:
        account_obj = await session.execute(select(Account).where(
            Account.name == account_name
        ))
        account = account_obj.scalars().first()
        income = Income(amount=amount, account_id=account.id)
        session.add(income)
        account.balance = account.balance + amount
        await session.commit()
