from decimal import Decimal
from typing import List, Tuple

from sqlalchemy.sql import extract, func, join, select

from src.tgbot_expenses.database.db import AsyncSessionWithEnter, database
from src.tgbot_expenses.models.expense_tracking_models import (Account,
                                                               Category,
                                                               Expense)


async def insert_expense(category_name: str, account_name: str,
                         amount: Decimal, telegram_id: int) -> None:
    """
    Insert a new financial transaction into the database.
    :param category_name: The name of the category of the transaction.
    :type category_name: str
    :param account_name: The name of the account from which
                         the transaction is made.
    :type account_name: str
    :param amount: The amount of the transaction.
    :type amount: Decimal
    :param telegram_id: The user's Telegram ID.
    :type telegram_id: int
    :return: None
    """
    async with AsyncSessionWithEnter(database.engine) as session:
        category_obj = await session.execute(select(Category).where(
            Category.user_id == telegram_id, Category.name == category_name
        ))
        category = category_obj.scalars().first()
        account_obj = await session.execute(select(Account).where(
            Account.user_id == telegram_id, Account.name == account_name
        ))
        account = account_obj.scalars().first()
        expense = Expense(amount=amount, category_id=category.id,
                          account_id=account.id, user_id=telegram_id)
        session.add(expense)
        await session.commit()


async def get_monthly_expenses(telegram_id: int) -> List[Tuple]:
    """
    Retrieve all the data for the current month from the 'expenses' and
    'categories' tables.
    :param telegram_id: The user's Telegram ID.
    :type telegram_id: int
    :return: A list of dictionaries containing the category name,
             monthli limit, total expenses for the month, and
             the current month.
    """
    async with AsyncSessionWithEnter(database.engine) as session:
        query = select(
            Category.name,
            Category.monthly_limit.label("limit_expenses"),
            func.sum(Expense.amount).label("total"),
            extract('month', Expense.date).label("month")
        ).select_from(
            join(Category, Expense, Category.id == Expense.category_id)
        ).where(
            Category.user_id == telegram_id,
            extract('year', Expense.date) == extract('year', func.now()),
            extract('month', Expense.date) == extract('month', func.now())
        ).group_by(Category.name,
                   Category.monthly_limit,
                   extract('month', Expense.date))

        rows = await session.execute(query)

        result = []
        for row in rows:
            dict_row = {}
            for index, column in enumerate(["category_name",
                                            "limit_expenses",
                                            "total", "month"]):
                dict_row[column] = row[index]
            result.append(dict_row)
        return result
