from decimal import Decimal
from typing import List, Tuple

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.sql import extract, func, select

from src.tgbot_expenses.config import Config
from src.tgbot_expenses.models.expense_tracking_models import (Account, Base,
                                                               Category,
                                                               Expense, Income)


class AsyncSessionWithEnter(AsyncSession):
    """
    Subclass of AsyncSession that provides support for the 'async with' syntax.

    Example usage:

    async with AsyncSessionWithEnter() as session:
        # interact with session object here

    """
    async def __aenter__(self):
        """
        Returns the session object when used in an 'async with' block.
        """
        return self

    async def __aexit__(self, exc_type, exc_val, traceback):
        """
        Rolls back any uncommitted changes when the 'async with' block
        is exited.
        """
        await super().__aexit__(exc_type, exc_val, traceback)


class AsyncPostgresDB:
    """
    An asynchronous database client for PostgreSQL.
    """
    _instance = None
    engine = None
    config = Config.load_config("bot.ini")

    def __new__(cls, *args, **kwargs):
        """
        Create a singleton instance of the AsyncPostgresDB class.

        :return: A singleton instance of the AsyncPostgresDB class.
        """
        if cls._instance is None:
            cls._instance = super(AsyncPostgresDB, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        """
        Initializes a new instance of the AsyncPostgresDB class.
        """
        if self.engine is None:
            db_config = self.config.postgres_db
            self.engine = create_async_engine(
                url=db_config.db_url,
                echo=True
            )

    async def __call__(self, *args, **kwargs) -> 'AsyncPostgresDB':
        """
        Returns the singleton instance of the AsyncPostgresDB class.
        """
        self.__init__(*args, **kwargs)
        return self.engine

    async def create_tables(self) -> None:
        """
        Creates the Category, Income, Expense, and Account tables
        if they do not exist.

        :return: None
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        return

    async def insert_expense(self, category_name: str,
                             account_name: str, amount: Decimal) -> None:
        """
        Insert a new financial transaction into the database.

        :param category_name: The name of the category of the transaction.
        :type category_name: str
        :param account_name: The name of the account from which the transaction
                             is made.
        :type account_name: str
        :param amount: The amount of the transaction.
        :type amount: Decimal
        :return: None
        """
        async with AsyncSessionWithEnter(self.engine) as session:
            category_obj = await session.execute(select(Category).where(
                Category.name == category_name
            ))
            category = category_obj.scalars().first()
            account_obj = await session.execute(select(Account).where(
                Account.name == account_name
            ))
            account = account_obj.scalars().first()
            expense = Expense(amount=amount, category_id=category.id,
                              account_id=account.id)
            session.add(expense)
            await session.commit()
        return

    async def insert_income(self, account_name: str, amount: Decimal) -> None:
        """
        Inserts a new income entry into the database for a given account.

        :param account_name: The name of the account for which to insert
                             the income.
        :type account_name: str
        :param amount: The amount of the income to insert.
        :type amount: Decimal
        :return: None
        """
        async with AsyncSessionWithEnter(self.engine) as session:
            account_obj = await session.execute(select(Account).where(
                Account.name == account_name
            ))
            account = account_obj.scalars().first()
            income = Income(amount=amount, account_id=account.id)
            session.add(income)
            account.balance = account.balance + amount
            await session.commit()
        return

    async def insert_account(self, account_name: str,
                             account_amount: Decimal) -> None:
        """
        Insert a new entry into the 'accounts' table with the given account
        name and account amount.

        :param account_name: The name of the account to insert.
        :type account_name: str
        :param account_amount: The amount associated with the account
                               to insert.
        :type account_amount: Decimal
        :return: None
        """
        async with AsyncSessionWithEnter(self.engine) as session:
            account = Account(name=account_name, balance=account_amount)
            session.add(account)
            await session.commit()
        return

    async def insert_category(self, category_name: str,
                              monthly_limit: Decimal) -> None:
        """
        Insert a new category entry into the 'categories' table with
        the given name and monthly limit.

        :param category_name: The name of the category to insert.
        :type category_name: str
        :param monthly limit: The limit amount for the category to insert.
        :type monthly limit: Decimal
        :return: None
        """
        async with AsyncSessionWithEnter(self.engine) as session:
            category = Category(name=category_name,
                                monthly_limit=monthly_limit)
            session.add(category)
            await session.commit()
        return

    async def get_monthly_limit(self, category_name: str) -> Decimal:
        """
        Retrieve the monthly limit for the given category from
        the 'categories' table.

        :param category_name: The name of the category to retrieve
                              the limit amount for.
        :type category_name: str
        :return: The monthly limit for the category.
        """
        async with AsyncSessionWithEnter(self.engine) as session:
            category_obj = await session.execute(select(Category).where(
                Category.name == category_name
            ))
            category = category_obj.scalars().first()
            monthly_limit = category.monthly_limit

            return monthly_limit

    async def get_amount(self, account_id: int) -> Decimal:
        """
        Retrieve the amount associated with the given account ID from
        the 'accounts' table.

        :param account_id: The ID of the account to retrieve the amount for.
        :type account_id: int
        :return: The balance associated with the account.
        """
        async with AsyncSessionWithEnter(self.engine) as session:
            account_obj = await session.execute(select(Account).where(
                Account.id == account_id
            ))
            account = account_obj.scalars().first()
            balance = account.balance

            return balance

    async def get_all_accounts(self) -> str:
        """
        Retrieve the names of all active accounts from the 'accounts' table.

        :return: A string containing the names of all active accounts,
                 separated by semicolons.
        """
        async with AsyncSessionWithEnter(self.engine) as session:
            accounts = await session.execute(select(Account.name).where(
                Account.account_status == "active"
            ))

            return ";".join([account[0] for account in accounts])

    async def get_all_categories(self) -> str:
        """
        Retrieve the names of all categories from the 'categories' table.

        :return: A string containing the names of all categories,
                 separated by semicolons.
        """
        async with AsyncSessionWithEnter(self.engine) as session:
            categories = await session.execute(select(Category.name).where(
                Category.category_status == "active"
            ))

            return ";".join([category[0] for category in categories])

    async def update_monthly_limit(self, category_name: str,
                                   new_limit: Decimal) -> None:
        """
        Update the monthly limit for the given category in the 'categories'
        table.

        :param category_name: The name of the category to update.
        :type category_name: str
        :param new_limit: The new monthly limit to set for the category.
        :type new_limit: Decimal
        :return: None
        """
        async with AsyncSessionWithEnter(self.engine) as session:
            category_obj = await session.execute(select(Category).where(
                Category.name == category_name
            ))
            category = category_obj.scalars().first()
            category.monthly_limit = new_limit
            await session.commit()
        return

    async def update_amount(self, account_from: str,
                            amount_old_currency: Decimal,
                            currency_amount: Decimal, account_to: str) -> None:
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
        :return: None
        """
        async with AsyncSessionWithEnter(self.engine) as session:
            account_obj_from = await session.execute(select(Account).where(
                Account.name == account_from
            ))
            account_from = account_obj_from.scalars().first()
            account_from.balance = account_from.balance - amount_old_currency

            account_obj_to = await session.execute(select(Account).where(
                Account.name == account_to
            ))
            account_to = account_obj_to.scalars().first()
            account_to.balance = account_to.balance + currency_amount
            await session.commit()
        return

    async def archive_account(self, account_name: str) -> None:
        """
        Update the status of the specified account to 'archive'
        in the 'accounts' table.

        :param account_name: The name of the account to be archived.
        :type account_name: str
        :return: None
        """
        async with AsyncSessionWithEnter(self.engine) as session:
            account_obj = await session.execute(select(Account).where(
                Account.name == account_name
            ))
            account = account_obj.scalars().first()
            account.account_status = "archive"
            await session.commit()
        return

    async def archive_category(self, category_name: str) -> None:
        """
        Update the status of the specified category to 'archive'
        in the 'categories' table.

        :param category_name: The name of the category to be archived.
        :type category_name: str
        :return: None
        """
        async with AsyncSessionWithEnter(self.engine) as session:
            category_obj = await session.execute(select(Category).where(
                Category.name == category_name
            ))
            category = category_obj.scalars().first()
            category.category_status = "archive"
            await session.commit()
        return

    async def get_monthly_expenses(self) -> List[Tuple]:
        """
        Retrieve all the data for the current month from the 'expenses' and
        'categories' tables.

        :return: A list of dictionaries containing the category name,
                 monthli limit, total expenses for the month,
                 and the current month.
        """
        async with AsyncSessionWithEnter(self.engine) as session:
            query = select(
                Category.name,
                Category.monthly_limit.label("limit_expenses"),
                func.sum(Expense.amount).label("total"),
                extract('month', Expense.date).label("month")
            ).where(
                Category.id == Expense.category_id,
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


database = AsyncPostgresDB()
