from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.helpers.keyboards.settings import get_keyboard_settings
from src.tgbot_expenses.states.chat_states import StateChat, StateSettings


@Bot.callback_query_handler(text="settings", state=StateChat.MainMenu)
async def callbacks_change_settings(query: types.CallbackQuery,
                                    state: FSMContext) -> None:
    """
    Handles the 'Settings' button press in the main menu, displaying
    settings which the user can change.

    :param query: The query object representing the button press.
    :type query: types.CallbackQuery
    :param state: The current state of the conversation.
    :type state: FSMContext
    :return: None
    """
    await query.message.delete()

    await StateSettings.next()

    await Bot.answer(
        message=query.message,
        text=QuestionText.main_menu,
        reply_markup=str(get_keyboard_settings())
    )
