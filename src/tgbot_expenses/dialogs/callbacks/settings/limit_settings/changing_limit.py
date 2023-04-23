from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.helpers.keyboards.question import get_keyboard_question
from src.tgbot_expenses.states.chat_states import StateSettings
from src.tgbot_expenses.utils.queries_database import \
    get_all_categories_with_retry


@Bot.callback_query_handler(text="change_limit", state=StateSettings.MainMenu)
async def callbacks_change_limit(query: types.CallbackQuery,
                                 state: FSMContext) -> None:
    """
    Handles the 'Change limit' button press in the settings menu,
    allowing the user to change the spending limit.

    :param query: The query object representing the button press.
    :type query: types.CallbackQuery
    :param state: The current state of the conversation.
    :type state: FSMContext
    :return: None
    """
    await query.message.delete()

    await StateSettings.ChangeLimit.set()

    categories = await get_all_categories_with_retry(
        telegram_id=query.from_user.id
    )
    await Bot.answer(
        message=query.message,
        text=QuestionText.limits,
        reply_markup=get_keyboard_question(
            button_names=categories,
            button_back=True
        )
    )
