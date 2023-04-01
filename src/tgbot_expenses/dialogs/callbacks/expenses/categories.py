from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.helpers.keyboards.question import get_keyboard_question
from src.tgbot_expenses.states.chat_states import StateChat


@Bot.callback_query_handler(state=StateChat.Category)
async def callbacks_get_category(query: types.CallbackQuery,
                                 state: FSMContext) -> None:
    """
    A callback function to handle the selection of a category. This function
    is triggered when a user selects a category from the list of available
    categories.

    :param query: The query object representing the button press.
    :type query: types.CallbackQuery
    :param state: The current state of the conversation.
    :type state: FSMContext
    :return: None
    """
    await query.message.delete()

    async with state.proxy() as data:
        data["category"] = query.data

    await StateChat.next()

    accounts = await database.get_all_accounts()

    await Bot.answer(
        message=query.message,
        text=QuestionText.bill,
        reply_markup=get_keyboard_question(
            button_names=accounts
        )
    )
