from contextlib import suppress

import aiogram
from aiogram import Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from aiogram.utils.exceptions import (BotBlocked, ChatNotFound,
                                      MessageCantBeDeleted,
                                      MessageToDeleteNotFound,
                                      TelegramAPIError, UserDeactivated)


class Bot:
    __instance: 'Bot' = None
    dispatch: Dispatcher = None
    bot = None

    def __new__(cls, *args, **kwargs) -> 'Bot':
        """
        Create singleton instance of Telegram Bot
        """
        if not cls.__instance:
            cls.__instance = super(Bot, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self, token: str = None, parse_mode: str = ParseMode.HTML):
        """
        Constructor initialize bot instance
        """
        if token is not None:
            self.bot = aiogram.Bot(token=token, parse_mode=parse_mode)
            self.dispatch = aiogram.Dispatcher(bot=self.bot,
                                               storage=MemoryStorage())

    def __call__(self, *args, **kwargs) -> Dispatcher:
        """
        Call bot as function constructor
        """
        self.__init__(*args, **kwargs)
        return self.dispatch

    def message_handler(self, *args, **kwargs):
        """
        Decorator for message handler
        """
        return self.dispatch.message_handler(*args, **kwargs)

    def callback_query_handler(self, *args, **kwargs):
        """
        Decorator for callback handler
        """
        return self.dispatch.callback_query_handler(*args, **kwargs)

    async def answer(self, message: types.Message, text: str, **kwargs):
        """
        Send text message to user
        """
        with suppress(BotBlocked, ChatNotFound,
                      UserDeactivated, TelegramAPIError):
            res = await message.answer(text=text, **kwargs)
        return res

    async def delete_message(self, chat_id: int, message_id: int):
        """
        Delete a bot message.
        """
        with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
            await self.bot.delete_message(chat_id=chat_id,
                                          message_id=message_id)

    async def delete_messages(self, chat_id: int,
                              last_message_id: int, count: int):
        """
        Delete bot messages.
        """
        for i in range(count):
            with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
                await self.bot.delete_message(chat_id=chat_id,
                                              message_id=last_message_id-i)

    async def get_current_state(self):
        """
        Get bot current state
        """
        return await self.dispatch.current_state().get_state()


Bot = Bot()
