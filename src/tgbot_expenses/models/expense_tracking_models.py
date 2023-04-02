from sqlalchemy import DECIMAL, Column, DateTime, ForeignKey, Integer, String
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

    id = Column(Integer, primary_key=True, index=True,  autoincrement=True)
    name = Column(String, nullable=False)
    monthly_limit = Column(DECIMAL, nullable=False)
    category_status = Column(String, nullable=False, default="active")

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

    id = Column(Integer, primary_key=True, index=True,  autoincrement=True)
    name = Column(String, nullable=False)
    balance = Column(DECIMAL, nullable=False)
    account_status = Column(String, nullable=False, default="active")

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

    id = Column(Integer, primary_key=True, index=True,  autoincrement=True)
    amount = Column(DECIMAL, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())

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

    id = Column(Integer, primary_key=True, index=True,  autoincrement=True)
    amount = Column(DECIMAL, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())

    account = relationship("Account", back_populates="incomes")
