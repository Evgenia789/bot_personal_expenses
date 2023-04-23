from asyncio import sleep

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from src.tgbot_expenses.bot import Bot


class UnrecognizedMessageMiddleware(BaseMiddleware):
    """
    Middleware to handle unknown messages or commands. If a message or command
    is not recognized, this middleware will send a response indicating that
    the message or command is not available.

    This middleware will not handle messages that are part of a conversation
    flow, as determined by the current state of the chat.
    """
    async def on_pre_process_message(self, message: types.Message,
                                     data: dict) -> None:
        """
        Handle unknown messages or commands. If the message or command
        is not recognized, send a response indicating that it is not available.

        :param message: The message to be processed.
        :type message: types.Message
        :param data: Additional data associated with the message.
        :type state: dict
        :return: None
        :raises CancelHandler: If the message is not recognized.
        """
        current_state = await Bot.get_current_state()

        # If the chat is in a conversation flow, do not handle unknown messages
        if current_state is None or (
            current_state.split(":")[-1] in ["Amount", "InvalidAmount",
                                             "NewLimit", "AddAccount",
                                             "CategoryLimit", "AddCategory",
                                             "AmountAccount",
                                             "FromAccountAmount",
                                             "ToAccountAmount"]
        ):
            return None

        # If the message is not recognized, send a response indicating that
        # it is not available
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


__all__ = ["UnrecognizedMessageMiddleware"]
