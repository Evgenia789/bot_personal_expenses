import logging

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.services.user_service import get_user_id


class AuthorizationMiddleware(BaseMiddleware):
    """
    Middleware to authorize users before processing messages.
    Only messages from authorized users will be processed.
    """
    async def on_pre_process_message(self, message: types.Message,
                                     data: dict) -> None:
        """
        Check if the message sender is an authorized user.
        If not, send a message indicating that the bot is not
        available to the user, to authorize, user should send,
        a message with the text "/init" and cancel the message handling.
        :param message: The message to be processed.
        :type message: types.Message
        :param data: Additional data associated with the message.
        :type state: dict
        :return: None
        :raises CancelHandler: If the message sender is not an authorized user.
        """
        await database.create_tables()
        try:
            user_id = await get_user_id(message.from_user.id)
        except Exception as e:
            logging.error("Failed to retrieve user ID: %s", e)
            user_id = None

        if message.text.rstrip() != "/init" and user_id is None:
            await message.delete()
            await Bot.answer(message=message, text=QuestionText.initialization)
            raise CancelHandler()


__all__ = ["AuthorizationMiddleware"]
