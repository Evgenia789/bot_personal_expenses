from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.helpers.keyboards.main_menu import \
    get_keyboard_main_menu
from src.tgbot_expenses.helpers.keyboards.start_over_or_continue import \
    get_keyboard_start_over_or_continue
from src.tgbot_expenses.states.chat_states import StateChat


class StartOrContinueMiddleware(BaseMiddleware):
    """
    Middleware to handle the '/start' command and the 'start_over' and
    'continue' buttons.

    If the current state is None and a message with the '/start' command is
    received, the middleware will delete the message and send a welcome message
    with the 'Start over' or 'Continue' buttons.

    If a callback query with 'start_over' or 'continue' is received, the
    middleware will delete the previous message and reset the state to the
    main menu (if 'start_over' is selected). Then, it will send the
    corresponding message and keyboard.

    If the current state is not None and the message is not a '/start' command,
    the middleware does nothing.
    """
    async def on_pre_process_message(self, message: types.Message,
                                     data: dict) -> None:
        """
        On pre process messages, check if the message is a "/start" command
        and there is a current state set for the user. If yes, delete the
        "/start" message, send a new message with a predefined text and a
        custom keyboard, and raise a CancelHandler exception to interrupt
        the further processing of the message.

        :param message: The incoming message.
        :type message: types.Message
        :param data: Additional data.
        :type data: dict
        :raises CancelHandler: If the message is a "/start" command and there
                               is a current state set for the user.
        """
        current_state = await Bot.get_current_state()

        if current_state is None:
            return None

        if message.content_type == "text" and "/start" == message.text.strip():
            await message.delete()

            await Bot.answer(
                message=message,
                text=QuestionText.start,
                reply_markup=str(get_keyboard_start_over_or_continue())
            )

            raise CancelHandler()

    async def on_pre_process_callback_query(self, query: types.CallbackQuery,
                                            data: dict) -> None:
        """
        On pre process callback query. If the callback query data
        is "start_over" or "continue", the corresponding message is deleted and
        the current state data is reset if the data is "start_over". The state
        is set to `StateChat.MainMenu`, and a new message is sent with the main
        menu options. Finally, a `CancelHandler` is raised to prevent further
        processing of the callback query.

        :param query: The callback query object
        :type query: types.CallbackQuery
        :param data: Additional data.
        :type data: dict
        :raises CancelHandler: Raised if the user clicks the "start over" or
                               "continue" button, in order to cancel further
                               processing of the callback query.
        """
        current_state = Bot.dispatch.current_state()

        if query.data in ["start_over", "continue"]:
            await Bot.delete_message(chat_id=query.message.chat.id,
                                     message_id=query.message.message_id)
            if query.data == "start_over":
                await Bot.delete_message(chat_id=query.message.chat.id,
                                         message_id=query.message.message_id-2)

                await current_state.reset_data()

                await StateChat.MainMenu.set()

                await Bot.answer(
                    message=query.message,
                    text=QuestionText.main_menu,
                    reply_markup=str(get_keyboard_main_menu())
                )

            raise CancelHandler()


__all__ = ["StartOrContinueMiddleware"]
