from typing import Union

from sqlalchemy.sql import select

from src.tgbot_expenses.database.db import AsyncSessionWithEnter, database
from src.tgbot_expenses.models.expense_tracking_models import User


async def insert_user(telegram_id: int) -> None:
    """
    Inserts a new user entry into the database for a given telegram ID.
    :param telegram_id: The user's Telegram ID.
    :type telegram_id: int
    :return: None
    """
    async with AsyncSessionWithEnter(database.engine) as session:
        user = User(id=telegram_id)
        session.add(user)
        await session.commit()


async def get_user_id(telegram_id: int) -> Union[int, None]:
    """
    Retrieve the id associated with the given telegram_id from
    the 'users' table.
    :param telegram_id: The user's Telegram ID.
    :type telegram_id: int
    :return: Union [int, None]
    """
    async with AsyncSessionWithEnter(database.engine) as session:
        result = await session.execute(select(User.id).where(
            User.id == telegram_id
        ))

        user_id = result.scalar_one_or_none()
        if user_id is None:
            return None
        else:
            return user_id
