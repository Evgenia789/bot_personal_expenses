from decimal import Decimal

from sqlalchemy.sql import select

from src.tgbot_expenses.database.db import AsyncSessionWithEnter, database
from src.tgbot_expenses.models.expense_tracking_models import Category


async def insert_category(category_name: str, monthly_limit: Decimal) -> None:
    """
    Insert a new category entry into the 'categories' table with
    the given name and monthly limit.

    :param category_name: The name of the category to insert.
    :type category_name: str
    :param monthly limit: The limit amount for the category to insert.
    :type monthly limit: Decimal
    :return: None
    """
    async with AsyncSessionWithEnter(database.engine) as session:
        category = Category(name=category_name,
                            monthly_limit=monthly_limit)
        session.add(category)
        await session.commit()

    return


async def get_monthly_limit(category_name: str) -> Decimal:
    """
    Retrieve the monthly limit for the given category from
    the 'categories' table.

    :param category_name: The name of the category to retrieve
                            the limit amount for.
    :type category_name: str
    :return: The monthly limit for the category.
    """
    async with AsyncSessionWithEnter(database.engine) as session:
        category_obj = await session.execute(select(Category).where(
            Category.name == category_name
        ))
        category = category_obj.scalars().first()
        monthly_limit = category.monthly_limit

        return monthly_limit


async def get_all_categories() -> str:
    """
    Retrieve the names of all categories from the 'categories' table.

    :return: A string containing the names of all categories,
                separated by semicolons.
    """
    async with AsyncSessionWithEnter(database.engine) as session:
        categories = await session.execute(select(Category.name).where(
            Category.category_status == "active"
        ))

        return ";".join([category[0] for category in categories])


async def update_monthly_limit(category_name: str, new_limit: Decimal) -> None:
    """
    Update the monthly limit for the given category in the 'categories'
    table.

    :param category_name: The name of the category to update.
    :type category_name: str
    :param new_limit: The new monthly limit to set for the category.
    :type new_limit: Decimal
    :return: None
    """
    async with AsyncSessionWithEnter(database.engine) as session:
        category_obj = await session.execute(select(Category).where(
            Category.name == category_name
        ))
        category = category_obj.scalars().first()
        category.monthly_limit = new_limit
        await session.commit()

    return


async def archive_category(category_name: str) -> None:
    """
    Update the status of the specified category to 'archive'
    in the 'categories' table.

    :param category_name: The name of the category to be archived.
    :type category_name: str
    :return: None
    """
    async with AsyncSessionWithEnter(database.engine) as session:
        category_obj = await session.execute(select(Category).where(
            Category.name == category_name
        ))
        category = category_obj.scalars().first()
        category.category_status = "archive"
        await session.commit()

    return