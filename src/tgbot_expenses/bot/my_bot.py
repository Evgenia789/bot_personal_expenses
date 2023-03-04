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
    """
    Singleton instance of a Telegram bot.

    This class provides a convenient interface to interact with the Telegram
    Bot API using the aiogram library. It creates a singleton instance of
    a bot and a dispatcher, which can be used to register message handlers
    and callback query handlers.

    To create a bot instance, simply call the `Bot()` constructor with your
    bot token:

    .. code-block:: python3

        bot = Bot(token='YOUR_BOT_TOKEN')

    You can then register message handlers and callback query handlers using
    the `message_handler()` and `callback_query_handler()` methods:

    .. code-block:: python3

        @bot.message_handler(commands=['start'])
        async def start_handler(message: types.Message):
            await bot.answer(message, "Hello, world!")

    The `answer()` method can be used to send text messages to users. You can
    also delete messages using the `delete_message()` and `delete_messages()`
    methods.

    The `get_current_state()` method can be used to get the current state of
    the bot.
    """
    __instance: 'Bot' = None
    dispatch: Dispatcher = None
    bot = None

    def __new__(cls, *args, **kwargs) -> 'Bot':
        """
        Create singleton instance of Telegram Bot.

        :return: A singleton instance of the Telegram Bot.
        """
        if not cls.__instance:
            cls.__instance = super(Bot, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self, token: str = None, parse_mode: str = ParseMode.HTML):
        """
        Initialize the bot instance with the given token and parse mode.

        :param token: The token of the Telegram bot to use.
        :type token: str, optional
        :param parse_mode: Send Markdown or HTML, if you want Telegram apps
                           to show bold, italic, fixed-width text or inline
                           URLs in your bot's message.
        :type parse_mode: :obj:`typing.Optional[base.String]`
        """
        if token is not None:
            self.bot = aiogram.Bot(token=token, parse_mode=parse_mode)
            self.dispatch = aiogram.Dispatcher(bot=self.bot,
                                               storage=MemoryStorage())

    def __call__(self, *args, **kwargs) -> Dispatcher:
        """
        Call bot as function constructor and return its dispatcher.

        :param args: Arguments to be passed to the __init__ method.
        :param kwargs: Keyword arguments to be passed to the __init__ method.
        :return: aiogram.Dispatcher: The bot's dispatcher.
        """
        self.__init__(*args, **kwargs)

        return self.dispatch

    def message_handler(self, *args, **kwargs):
        """
        The message_handler method is a decorator for registering message
        handlers for the bot. It takes in one or more args and kwargs as
        parameters that can be used to specify the type of messages the
        handler should handle.

        Examples:

        Simple commands handler:

        .. code-block:: python3

            @Bot.message_handler(commands=['start', 'welcome', 'about'])
            async def cmd_handler(message: types.Message):

        :param args: Additional arguments that can be used to specify the type
                     of messages the handler should handle.
        :param kwargs: Additional keyword arguments that can be used to specify
                       the type of messages the handler should handle.
        :return: A decorated function that can be used to handle incoming
                 messages.
        """
        return self.dispatch.message_handler(*args, **kwargs)

    def callback_query_handler(self, *args, **kwargs):
        """
        The callback_handler methodis a decorator that registers a callback
        function to be executed when a user taps a callback button. It takes
        in one or more args and kwargs as parameters that can be used to
        specify the type of messages the handler should handle.

        Example:

        .. code-block:: python3

            @Bot.callback_query_handler(lambda callback_query: True)
            async def some_callback_handler(query: types.CallbackQuery)

        :param args: Additional arguments that can be used to specify the type
                     of callback queries the handler should handle.
        :param kwargs: Additional keyword arguments that can be used to specify
                       the type of callback queries the handler should handle.
        :return: A decorated function that can be used to handle incoming
                 callback queries.
        """
        return self.dispatch.callback_query_handler(*args, **kwargs)

    async def answer(self, message: types.Message, text: str, **kwargs):
        """
        Send a text message to a user.

        :param message: The message object to respond to.
        :type message: types.Message
        :param text: The text of the message to send.
        :type text: str
        :param kwargs: Additional arguments to pass to `message.answer()`.
        :return: The sent message object, or `None`
                 if the message was not sent.
        """
        with suppress(BotBlocked, ChatNotFound,
                      UserDeactivated, TelegramAPIError):
            return await message.answer(text=text, **kwargs)

    async def delete_message(self, chat_id: int, message_id: int):
        """
        Delete a message in a chat.

        :param chat_id: The ID of the chat where the message to be deleted
                        is located.
        :type chat_id: :obj:`typing.Union[base.Integer, base.String]`
        :param message_id: The ID of the message to be deleted.
        :type message_id: :obj:`base.Integer`
        :return: None.
        """
        with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
            await self.bot.delete_message(chat_id=chat_id,
                                          message_id=message_id)

    async def delete_messages(self, chat_id: int,
                              last_message_id: int, count: int):
        """
        Delete multiple messages in a chat.

        :param chat_id: The ID of the chat the messages belong to.
        :type chat_id: :obj:`typing.Union[base.Integer, base.String]`
        :param last_message_id: The ID of the last message to delete.
        :type last_message_id: :obj:`base.Integer`
        :param count: The number of messages to delete.
        :type count: int
        :return: None
        """
        for i in range(count):
            with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
                await self.bot.delete_message(chat_id=chat_id,
                                              message_id=last_message_id-i)

    async def get_current_state(self):
        """
        Get the current state of the bot's dispatcher.

        :return: A string representing the current state of the bot's
                 dispatcher.
        """
        return await self.dispatch.current_state().get_state()


Bot = Bot()
