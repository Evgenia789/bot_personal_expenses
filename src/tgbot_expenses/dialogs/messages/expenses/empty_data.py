from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.helpers.keyboards.back_or_main_menu import \
    get_keyboard_back_or_main_menu
from src.tgbot_expenses.states.chat_states import StateChat, StateEmpty


@Bot.message_handler(state=StateEmpty.InvalidEmpty)
async def message_empty_data(message: types.Message,
                             state: FSMContext) -> None:
    """
    Responds to a user message when there is no data available
    in the database.

    :param message: The user's message to respond to.
    :type message: types.Message
    :param state: The current state of the conversation.
    :type state: FSMContext
    :return: None
    """
    await StateChat.MainMenu.set()

    await Bot.answer(
        message=message,
        text=QuestionText.empty_data,
        reply_markup=str(get_keyboard_back_or_main_menu(back_button=False))
    )
