from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.dialogs.callbacks.start_or_continue import (
    callbacks_continue, callbacks_start_over)
from src.tgbot_expenses.helpers.keyboards.changing_bill import \
    get_keyboard_changing_bill
from src.tgbot_expenses.states.states_settings import StateSettings


@Bot.callback_query_handler(text="change_bill", state=StateSettings.MainMenu)
async def callbacks_bill(query: types.CallbackQuery,
                         state: FSMContext) -> None:
    """
    Process of changing a bill.
    """
    await query.message.delete()

    await StateSettings.ChangeBill.set()
        
    await Bot.answer(
        query.message,
        QuestionText.bills,
        reply_markup=str(get_keyboard_changing_bill())
    )
