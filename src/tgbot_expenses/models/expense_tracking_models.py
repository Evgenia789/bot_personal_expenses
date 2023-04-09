import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Category(Base):
    """
    Represents a spending category, with a name and monthly spending limit.

    Attributes:
        id (int): primary key identifier for the category
        name (str): name of the category
        monthly_limit (Decimal): maximum amount that can be spent in this
                                 category per month
        category_status (str): status of the category, defaults to "active"

    Relationships:
        expenses (List[Expense]): all expenses that belong to this category
    """
    __tablename__ = 'categories'

    id = sa.Column(sa.Integer, primary_key=True, index=True,
                   autoincrement=True)
    name = sa.Column(sa.String(30), nullable=False)
    monthly_limit = sa.Column(sa.DECIMAL, nullable=False)
    category_status = sa.Column(sa.String(10), nullable=False,
                                default="active")

    expenses = relationship("Expense", back_populates="category")


class Account(Base):
    """
    Represents a financial account, with a name and current balance.

    Attributes:
        id (int): primary key identifier for the account
        name (str): name of the account
        balance (Decimal): current balance of the account
        account_status (str): status of the account, defaults to "active"

    Relationships:
        expenses (List[Expense]): all expenses that belong to this account
        incomes (List[Income]): all incomes that belong to this account
    """
    __tablename__ = 'accounts'

    id = sa.Column(sa.Integer, primary_key=True, index=True,
                   autoincrement=True)
    name = sa.Column(sa.String(50), nullable=False)
    balance = sa.Column(sa.DECIMAL, nullable=False)
    account_status = sa.Column(sa.String(10), nullable=False, default="active")

    expenses = relationship("Expense", back_populates="account")
    incomes = relationship("Income", back_populates="account")


class Expense(Base):
    """
    Represents a single expense transaction, with an amount, date, and
    the category and account it belongs to.

    Attributes:
        id (int): primary key identifier for the expense transaction
        amount (Decimal): amount of the expense transaction
        category_id (int): foreign key reference to the category this
                           expense belongs to
        account_id (int): foreign key reference to the account this
                          expense belongs to
        date (datetime): date and time the expense occurred

    Relationships:
        category (Category): the category that this expense belongs to
        account (Account): the account that this expense belongs to
    """
    __tablename__ = 'expenses'

    id = sa.Column(sa.Integer, primary_key=True, index=True,
                   autoincrement=True)
    amount = sa.Column(sa.DECIMAL, nullable=False)
    category_id = sa.Column(sa.Integer, sa.ForeignKey("categories.id"),
                            nullable=False)
    account_id = sa.Column(sa.Integer, sa.ForeignKey("accounts.id"),
                           nullable=False)
    date = sa.Column(sa.DateTime(timezone=True), server_default=func.now())

    category = relationship("Category", back_populates="expenses")
    account = relationship("Account", back_populates="expenses")


class Income(Base):
    """
    Represents a single income transaction, with an amount, date, and
    the account it belongs to.

    Attributes:
        id (int): primary key identifier for the income transaction
        amount (Decimal): amount of the income transaction
        account_id (int): foreign key reference to the account this
                          income belongs to
        date (datetime): date and time the income was received

    Relationships:
        account (Account): the account that this income belongs to
    """
    __tablename__ = 'incomes'

    id = sa.Column(sa.Integer, primary_key=True, index=True,
                   autoincrement=True)
    amount = sa.Column(sa.DECIMAL, nullable=False)
    account_id = sa.Column(sa.Integer, sa.ForeignKey("accounts.id"),
                           nullable=False)
    date = sa.Column(sa.DateTime(timezone=True), server_default=func.now())

    account = relationship("Account", back_populates="incomes")
