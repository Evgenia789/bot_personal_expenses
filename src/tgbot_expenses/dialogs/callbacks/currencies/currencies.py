from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.helpers.keyboards.question import get_keyboard_question
from src.tgbot_expenses.states.chat_states import (StateChat,
                                                   StateCurrencyExchange)


@Bot.callback_query_handler(text="exchange_currency", state=StateChat.MainMenu)
async def callbacks_exchange_currency(query: types.CallbackQuery,
                                      state: FSMContext) -> None:
    """
    A callback function to handle the starting of a currency exchange process.
    This function is triggered when a user selects the "Exchange currency"
    option from the main menu.

    :param query: The query object representing the button press.
    :type query: types.CallbackQuery
    :param state: The current state of the conversation.
    :type state: FSMContext
    :return: None
    """
    await query.message.delete()

    await StateCurrencyExchange.FromBill.set()

    accounts = await database.get_all_accounts()
    await Bot.answer(
        message=query.message,
        text=QuestionText.from_bill,
        reply_markup=get_keyboard_question(
            button_names=accounts,
            button_back=True
        )
    )
