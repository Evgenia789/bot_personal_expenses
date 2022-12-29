from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.dialogs.callbacks.start_or_continue import (
    callbacks_continue, callbacks_start_over)
from src.tgbot_expenses.helpers.keyboards.back_or_main_menu import \
    get_keyboard_back_or_main_menu
from src.tgbot_expenses.states.states_settings import StateSettings


@Bot.callback_query_handler(text="add_bill", state=StateSettings.ChangeBill)
async def callbacks_settings(query: types.CallbackQuery,
                             state: FSMContext) -> None:
    """
    Process main menu buttons.
    """
    await query.message.delete()

    await StateSettings.AddBill.set()
        
    await Bot.answer(
        query.message,
        QuestionText.new_bill,
        reply_markup=str(get_keyboard_back_or_main_menu(main_menu_button=False))
    )
