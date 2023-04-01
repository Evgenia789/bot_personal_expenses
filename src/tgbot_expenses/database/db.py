from decimal import Decimal
from typing import List, Tuple

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import extract, func

from src.tgbot_expenses.config import load_config
from src.tgbot_expenses.models.expense_tracking_models import (Account, Base,
                                                               Category,
                                                               Expense, Income)


class AsyncPostgresDB:
    """
    An asynchronous database client for PostgreSQL.

    Attributes:
        db_url (str): The URL for connecting to the PostgreSQL database.
        engine (sqlalchemy.engine.Engine): The SQLAlchemy engine object
                                           for the database.
        SessionLocal (sqlalchemy.orm.session.sessionmaker): The SQLAlchemy
                                                            sessionmaker object
                                                            for the database.
    """
    _instance = None
    engine = None
    SessionLocal = None
    config = load_config("bot.ini")

    def __new__(cls, *args, **kwargs):
        """
        Create a singleton instance of the Database class.
        :return: A singleton instance of the Database class.
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
            self.db_url = self.config.postgres_db.db_url
            self.engine = create_engine(self.db_url, echo=True, future=True)
            self.SessionLocal = sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=self.engine,
                                             class_=AsyncSession)
            self.create_tables()

    async def get_session(self):
        """
        Creates a new session for interacting with the database.

        Yields:
            sqlalchemy.ext.asyncio.AsyncSession: The new session object.
        """
        async with self.engine.begin() as conn:
            session = self.SessionLocal(bind=conn)
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    def __call__(self) -> "AsyncPostgresDB":
        """
        Returns the singleton instance of the AsyncPostgresDB class.
        """
        if self._instance is None:
            self._instance = AsyncPostgresDB()
        return self._instance

    async def create_tables(self):
        """
        Creates the Category, Income, Expense, and Account tables
        if they do not exist.
        """
        async with self.get_session() as session:
            for table in [Category.__table__, Income.__table__,
                          Expense.__table__, Account.__table__]:
                exists = await session.run_sync(table.exists)
                if not exists:
                    await session.run_sync(Base.metadata.create_all,
                                           tables=[table])

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
        """
        async with self.get_session() as session:
            category = session.query(Category)\
                              .filter_by(name=category_name).first()
            account = session.query(Account)\
                             .filter_by(name=account_name).first()
            expense = Expense(amount=amount, category_id=category.id,
                              account_id=account.id)
            session.add(expense)

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
        async with self.get_session() as session:
            account = session.query(Account).filter_by(
                name=account_name
            ).first()
            income = Income(amount=amount, account_id=account.id)
            session.add(income)

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
        async with self.get_session() as session:
            account = Account(name=account_name, balance=account_amount)
            session.add(account)

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
        async with self.get_session() as session:
            category = Category(name=category_name,
                                monthly_limit=monthly_limit)
            session.add(category)

    async def get_monthly_limit(self, category_name: str) -> Decimal:
        """
        Retrieve the monthly limit for the given category from
        the 'categories' table.

        :param category_name: The name of the category to retrieve
                              the limit amount for.
        :type category_name: str
        :return: The monthly limit for the category.
        """
        async with self.get_session() as session:
            category = session.query(Category)\
                       .filter_by(name=category_name).first()
            monthly_limit = category.monthly_limit

            return monthly_limit

    async def get_amount(self, account_id: int) -> Decimal:
        """
        Retrieve the amount associated with the given account ID from
        the 'accounts' table.

        :param account_id: The ID of the account to retrieve the amount for.
        :type account_id: int
        :return: The amount associated with the account.
        """
        async with self.get_session() as session:
            account = session.query(Account).filter_by(id=account_id).first()
            amount = account.amount

            return amount

    async def get_all_accounts(self) -> str:
        """
        Retrieve the names of all active accounts from the 'accounts' table.

        :return: A string containing the names of all active accounts,
                 separated by semicolons.
        """
        async with self.get_session() as session:
            accounts = session.query(Account.name)\
                              .filter_by(account_status="active").all()

            return ";".join([account for account in accounts])

    async def get_all_categories(self) -> str:
        """
        Retrieve the names of all categories from the 'categories' table.

        :return: A string containing the names of all categories,
                 separated by semicolons.
        """
        async with self.get_session() as session:
            categories = session.query(Category.name)\
                                .filter_by(category_status="active").all()

            return ";".join([category for category in categories])

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
        async with self.get_session() as session:
            session.query(Category).filter_by(name=category_name).update(
                {"monthly_limit": new_limit}
            )

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
        async with self.get_session() as session:
            account_first = session.query(Account)\
                                   .filter_by(name=account_from).first()
            account_first.amount = account_first.amount - amount_old_currency

            account_second = session.query(Account)\
                                    .filter_by(name=account_to).first()
            account_second.amount = account_second.amount + currency_amount

    async def archive_account(self, account_name: str) -> None:
        """
        Update the status of the specified account to 'archive'
        in the 'accounts' table.

        :param account_name: The name of the account to be archived.
        :type account_name: str
        :return: None
        """
        async with self.get_session() as session:
            session.query(Account).filter_by(name=account_name).update(
                {"account_status": "archive"}
            )

    async def archive_category(self, category_name: str) -> None:
        """
        Update the status of the specified category to 'archive'
        in the 'categories' table.

        :param category_name: The name of the category to be archived.
        :type category_name: str
        :return: None
        """
        async with self.get_session() as session:
            session.query(Category).filter_by(name=category_name).update(
                {"category_status": "archive"}
            )

    async def get_monthly_expenses(self) -> List[Tuple]:
        """
        Retrieve all the data for the current month from the 'expenses' and
        'categories' tables.

        :return: A list of dictionaries containing the category name,
                 monthli limit, total expenses for the month,
                 and the current month.
        """
        async with self.get_session() as session:
            rows = session.query(
                Category.name,
                Category.monthly_limit.label("limit_expenses"),
                func.sum(Expense.amount).label("total"),
                extract('month', Expense.date).label("month")
            ).filter(
                Category.id == Expense.category_id,
                extract('year', Expense.date) == extract('year', func.now()),
                extract('month', Expense.date) == extract('month', func.now())
            ).group_by(Category.name, Category.monthly_limit)

        result = []
        for row in rows:
            dict_row = {}
            for index, column in enumerate(["category_name", "limit_expenses",
                                           "total", "month"]):
                dict_row[column] = row[index]
            result.append(dict_row)
        return result


database = AsyncPostgresDB()
