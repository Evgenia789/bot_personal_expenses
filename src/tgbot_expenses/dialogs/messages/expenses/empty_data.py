import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.helpers.keyboards.main_menu import \
    get_keyboard_main_menu
from src.tgbot_expenses.states.chat_states import StateChat


@Bot.message_handler(state=StateChat.MainMenu)
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
    message_warning = await message.answer(QuestionText.empty_data)

    await asyncio.sleep(5)

    await message_warning.delete()

    await Bot.answer(
        message=message,
        text=QuestionText.main_menu,
        reply_markup=str(get_keyboard_main_menu())
    )
