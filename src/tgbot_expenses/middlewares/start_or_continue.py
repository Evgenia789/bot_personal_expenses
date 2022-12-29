import asyncio

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.config import load_config

config = load_config("bot.ini")


class StartOrContinueMiddleware(BaseMiddleware):
    """Start or continue middleware"""
    async def on_pre_process_message(self, message: types.Message, data: dict) -> None:
        """
        On pre process messages
        """
        if message.from_id not in config.ids:
            message = await message.answer("Sorry, this bot is not available to you 😔")
            await asyncio.sleep(2)
            await Bot.delete_messages(message.chat.id, message.message_id, 2)
            raise CancelHandler()

        current_state = await Bot.get_current_state()

        if current_state is None:
            return None

        if message.content_type == "text" and "/start" == message.text.strip():
            await message.delete()

            keyboard = types.InlineKeyboardMarkup(row_width=2).add(
                types.InlineKeyboardButton(
                    text="Start over",
                    callback_data="start_over"),
                types.InlineKeyboardButton(
                    text="Continue",
                    callback_data="continue")
            )
            await message.answer(("You are in the process of entering expenses"),
                                 reply_markup=str(keyboard))
            raise CancelHandler()


__all__ = ["StartOrContinueMiddleware"]
