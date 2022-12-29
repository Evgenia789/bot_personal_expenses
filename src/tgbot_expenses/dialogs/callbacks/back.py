from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.dialogs.callbacks.start_or_continue import (
    callbacks_continue, callbacks_start_over)
from src.tgbot_expenses.helpers.keyboards.question import \
    get_keyboard_question
from src.tgbot_expenses.helpers.keyboards.settings import \
    get_keyboard_settings
from src.tgbot_expenses.helpers.keyboards.changing_bill import \
    get_keyboard_changing_bill
from src.tgbot_expenses.helpers.keyboards.main_menu import \
    get_keyboard_main_menu
from src.tgbot_expenses.states.states_settings import StateSettings
from src.tgbot_expenses.states.states_chat import StateChat


@Bot.callback_query_handler(text="back", state="*")
async def callbacks_back(query: types.CallbackQuery,
                         state: FSMContext) -> None:
    """
    Process back button.
    """
    await query.message.delete()

    current_state = await Bot.get_current_state()
    current_state_name = current_state.split(":")[-1]    

    if current_state_name == "Category":
        await StateChat.previous()
        question = QuestionText.main_menu
        keyboard = str(get_keyboard_main_menu())
    else:
        await StateSettings.previous()

        if current_state_name in ["ChangeLimit", "ChangeBill"]:
            question, keyboard = QuestionText.main_menu, get_keyboard_settings()
            if current_state_name == "ChangeBill":
                await StateSettings.MainMenu.set()
        elif current_state_name == "NewLimit":
            question = QuestionText.limits
            keyboard = get_keyboard_question(
                button_names=(database.get_all_categories()),
                button_back=True
            )
        elif current_state_name in ["AddBill", "DeleteBill"]:
            question, keyboard = QuestionText.bills, get_keyboard_changing_bill()
            if current_state_name == "DeleteBill":
                await StateSettings.ChangeBill.set()

    await Bot.answer(
        query.message,
        text=question,
        reply_markup=str(keyboard)
    )
