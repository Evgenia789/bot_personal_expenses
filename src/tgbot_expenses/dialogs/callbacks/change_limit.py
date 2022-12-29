from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.dialogs.callbacks.back import callbacks_back
from src.tgbot_expenses.dialogs.callbacks.start_or_continue import (
    callbacks_continue, callbacks_start_over)
from src.tgbot_expenses.helpers.keyboards.question import \
    get_keyboard_question
from src.tgbot_expenses.states.states_settings import StateSettings


@Bot.callback_query_handler(text="change_limit", state=StateSettings.MainMenu)
async def callbacks_change_limit(query: types.CallbackQuery,
                                 state: FSMContext) -> None:
    """
    Process of changing a limit.
    """
    await query.message.delete()

    await StateSettings.ChangeLimit.set()

    await Bot.answer(
        query.message,
        QuestionText.limits,
        reply_markup=get_keyboard_question(
            button_names=(database.get_all_categories()),
            button_back=True
        )
    )
