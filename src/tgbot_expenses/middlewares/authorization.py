import asyncio

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.config import load_config


class AuthorizationMiddleware(BaseMiddleware):
    """Authorization middleware"""
    async def on_pre_process_message(self, message: types.Message,
                                     data: dict) -> None:
        """
        On pre process messages
        """
        config = load_config("bot.ini")

        if message.from_id not in [config.ids.id_1, config.ids.id_2]:

            message = await Bot.answer(
                message=message,
                text="Sorry, this bot is not available to you 😔"
            )

            await asyncio.sleep(2)

            await Bot.delete_messages(chat_id=message.chat.id,
                                      message_id=message.message_id, count=2)

            raise CancelHandler()


__all__ = ["AuthorizationMiddleware"]
