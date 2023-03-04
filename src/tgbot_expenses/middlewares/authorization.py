import asyncio

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.config import load_config


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
        available to the user and cancel the message handling.

        :param message: The message to be processed.
        :type message: types.Message
        :param data: Additional data associated with the message.
        :type state: dict
        :return: None
        :raises CancelHandler: If the message sender is not an authorized user.
        """
        config = load_config("bot.ini")

        if message.from_user.id not in [config.ids.id_1, config.ids.id_2]:

            response = await Bot.answer(
                message=message,
                text="Sorry, this bot is not available to you 😔"
            )

            await asyncio.sleep(2)

            await Bot.delete_messages(chat_id=response.chat.id,
                                      message_id=response.message_id, count=2)

            raise CancelHandler()


__all__ = ["AuthorizationMiddleware"]
