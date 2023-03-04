from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.helpers.keyboards.changing_bill import \
    get_keyboard_changing_bill
from src.tgbot_expenses.helpers.keyboards.changing_category import \
    get_keyboard_changing_category
from src.tgbot_expenses.helpers.keyboards.main_menu import \
    get_keyboard_main_menu
from src.tgbot_expenses.helpers.keyboards.question import get_keyboard_question
from src.tgbot_expenses.helpers.keyboards.settings import get_keyboard_settings
from src.tgbot_expenses.states.chat_states import StateChat, StateSettings


@Bot.callback_query_handler(text="back", state="*")
async def callbacks_back(query: types.CallbackQuery,
                         state: FSMContext) -> None:
    """
    Handles the 'back' button press in various states of the conversation,
    allowing the user to navigate to the previous screen.

    :param query: The query object representing the button press.
    :type query: types.CallbackQuery
    :param state: The current state of the conversation.
    :type state: FSMContext
    :return: None
    """
    await query.message.delete()

    current_state = await Bot.get_current_state()
    current_state_name = current_state.split(":")[-1]

    if current_state_name in ["Bill", "Category"]:
        await StateChat.MainMenu.set()
        question = QuestionText.main_menu
        keyboard = str(get_keyboard_main_menu())
    else:
        await StateSettings.previous()

        if current_state_name in ["ChangeLimit", "ChangeBill",
                                  "ChangeCategory"]:
            question = QuestionText.main_menu
            keyboard = get_keyboard_settings()
            if current_state_name in ["ChangeBill", "ChangeCategory"]:
                await StateSettings.MainMenu.set()
        elif current_state_name == "NewLimit":
            question = QuestionText.limits
            keyboard = get_keyboard_question(
                button_names=(database.get_all_categories()),
                button_back=True
            )
        elif current_state_name in ["AddBill", "DeleteBill"]:
            question = QuestionText.changing
            keyboard = get_keyboard_changing_bill()
            if current_state_name == "DeleteBill":
                await StateSettings.ChangeBill.set()
        elif current_state_name in ["AddCategory", "DeleteCategory"]:
            question = QuestionText.changing
            keyboard = get_keyboard_changing_category()
            if current_state_name == "DeleteCategory":
                await StateSettings.ChangeCategory.set()

    await Bot.answer(
        message=query.message,
        text=question,
        reply_markup=str(keyboard)
    )
