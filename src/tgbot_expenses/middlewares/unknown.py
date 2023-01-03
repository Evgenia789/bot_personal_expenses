from asyncio import sleep

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from src.tgbot_expenses.bot import Bot


class UnknownMiddleware(BaseMiddleware):
    """Unknown middleware"""
    async def on_pre_process_message(self, message: types.Message,
                                     data: dict) -> None:
        """
        On pre process messages
        """
        current_state = await Bot.get_current_state()

        if current_state is None or (
            current_state.split(":")[-1] in ["Amount", "InvalidAmount",
                                             "NewLimit", "AddBill"]
        ):
            return None

        if message.text:
            text = "This command is not available" if "/" == message.text[0] \
                else "Message not recognized"
        else:
            text = "The bot does not accept files."

        new_message = await message.reply(text)

        await sleep(2)
        await message.delete()
        await new_message.delete()

        raise CancelHandler()


__all__ = ["UnknownMiddleware"]
