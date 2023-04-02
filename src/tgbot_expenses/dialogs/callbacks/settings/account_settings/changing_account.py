from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.helpers.keyboards.changing_account import \
    get_keyboard_changing_account
from src.tgbot_expenses.states.chat_states import StateSettings


@Bot.callback_query_handler(text="change_account",
                            state=StateSettings.MainMenu)
async def callbacks_change_account(query: types.CallbackQuery,
                                   state: FSMContext) -> None:
    """
    Handles the 'Change account' button press in the settings menu,
    allowing the user to change an account to the list.

    :param query: The query object representing the button press.
    :type query: types.CallbackQuery
    :param state: The current state of the conversation.
    :type state: FSMContext
    :return: None
    """
    await query.message.delete()

    await StateSettings.ChangeAccount.set()

    await Bot.answer(
        message=query.message,
        text=QuestionText.changing,
        reply_markup=str(get_keyboard_changing_account())
    )
