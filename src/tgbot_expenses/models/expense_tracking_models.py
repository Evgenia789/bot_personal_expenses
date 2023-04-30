import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    """
    Represents a user.
    Attributes:
        id (int): identifier for the user via telegram_id as a primary key.
    Relationships:
        categories (List[Category]): the categories that belong to this user
        accounts (List[Account]): the accounts that belong to this user
        expenses (List[Expense]): the expenses that belong to this user
        incomes (List[Income]): the incomes that belong to this user
    """
    __tablename__ = 'users'

    id = sa.Column(sa.BigInteger, primary_key=True, index=True)

    categories = relationship("Category", back_populates="users")
    accounts = relationship("Account", back_populates="users")
    expenses = relationship("Expense", back_populates="users")
    incomes = relationship("Income", back_populates="users")


class Category(Base):
    """
    Represents a spending category, with a name and monthly spending limit.

    Attributes:
        id (int): primary key identifier for the category
        name (str): name of the category
        monthly_limit (Decimal): maximum amount that can be spent in this
                                 category per month
        category_status (str): status of the category, defaults to "active"
        user_id (int): foreign key reference to the user this
                       expense belongs to

    Relationships:
        expenses (List[Expense]): the expenses that belong to this category
        users (List[User]): thel users that belong to this category
    """
    __tablename__ = 'categories'

    id = sa.Column(sa.Integer, primary_key=True, index=True,
                   autoincrement=True)
    name = sa.Column(sa.String(30), nullable=False)
    monthly_limit = sa.Column(sa.DECIMAL, nullable=False)
    category_status = sa.Column(sa.String(10), nullable=False,
                                default="active")
    user_id = sa.Column(sa.BigInteger, sa.ForeignKey("users.id"),
                        nullable=False)

    expenses = relationship("Expense", back_populates="categories")
    users = relationship("User", back_populates="categories")


class Account(Base):
    """
    Represents a financial account, with a name and current balance.

    Attributes:
        id (int): primary key identifier for the account
        name (str): name of the account
        balance (Decimal): current balance of the account
        account_status (str): status of the account, defaults to "active"
        user_id (int): foreign key reference to the user this
                       expense belongs to

    Relationships:
        expenses (List[Expense]): the expenses that belong to this account
        incomes (List[Income]): the incomes that belong to this account
        users (List[User]): the users that belong to this account
    """
    __tablename__ = 'accounts'

    id = sa.Column(sa.Integer, primary_key=True, index=True,
                   autoincrement=True)
    name = sa.Column(sa.String(50), nullable=False)
    balance = sa.Column(sa.DECIMAL, nullable=False)
    account_status = sa.Column(sa.String(10), nullable=False, default="active")
    user_id = sa.Column(sa.BigInteger, sa.ForeignKey("users.id"),
                        nullable=False)

    expenses = relationship("Expense", back_populates="accounts")
    incomes = relationship("Income", back_populates="accounts")
    users = relationship("User", back_populates="accounts")


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
        user_id (int): foreign key reference to the user this
                       expense belongs to

    Relationships:
        category (Category): the categories that this expense belongs to
        account (Account): the accounts that this expense belongs to
        users (User): the users that this expense belongs to
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
    user_id = sa.Column(sa.BigInteger, sa.ForeignKey("users.id"),
                        nullable=False)

    categories = relationship("Category", back_populates="expenses")
    accounts = relationship("Account", back_populates="expenses")
    users = relationship("User", back_populates="expenses")


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
        user_id (int): foreign key reference to the user this
                       income belongs to

    Relationships:
        account (Account): the account that this income belongs to
        users (User): the users that this income belongs to
    """
    __tablename__ = 'incomes'

    id = sa.Column(sa.Integer, primary_key=True, index=True,
                   autoincrement=True)
    amount = sa.Column(sa.DECIMAL, nullable=False)
    account_id = sa.Column(sa.Integer, sa.ForeignKey("accounts.id"),
                           nullable=False)
    date = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
    user_id = sa.Column(sa.BigInteger, sa.ForeignKey("users.id"),
                        nullable=False)

    accounts = relationship("Account", back_populates="incomes")
    users = relationship("User", back_populates="incomes")
