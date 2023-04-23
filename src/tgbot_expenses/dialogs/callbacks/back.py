from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.helpers.keyboards.changing_account import \
    get_keyboard_changing_account
from src.tgbot_expenses.helpers.keyboards.changing_category import \
    get_keyboard_changing_category
from src.tgbot_expenses.helpers.keyboards.main_menu import \
    get_keyboard_main_menu
from src.tgbot_expenses.helpers.keyboards.question import get_keyboard_question
from src.tgbot_expenses.helpers.keyboards.settings import get_keyboard_settings
from src.tgbot_expenses.states.chat_states import StateChat, StateSettings
from src.tgbot_expenses.utils.queries_database import \
    get_all_categories_with_retry


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

    if current_state_name in ["Account", "Category",
                              "FromAccount", "ToAccount"]:
        await StateChat.MainMenu.set()
        question = QuestionText.main_menu
        keyboard = str(get_keyboard_main_menu())
    else:
        await StateSettings.previous()

        if current_state_name in ["ChangeLimit", "ChangeAccount",
                                  "ChangeCategory"]:
            question = QuestionText.main_menu
            keyboard = get_keyboard_settings()
            if current_state_name in ["ChangeAccount", "ChangeCategory"]:
                await StateSettings.MainMenu.set()
        elif current_state_name == "NewLimit":
            question = QuestionText.limits
            categories = await get_all_categories_with_retry(
                telegram_id=query.from_user.id
            )
            keyboard = get_keyboard_question(
                button_names=(categories),
                button_back=True
            )
        elif current_state_name in ["AddAccount", "DeleteAccount"]:
            question = QuestionText.changing
            keyboard = get_keyboard_changing_account()
            if current_state_name == "DeleteAccount":
                await StateSettings.ChangeAccount.set()
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
