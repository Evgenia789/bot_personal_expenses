from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.states.chat_states import StateChat


@Bot.callback_query_handler(state=StateChat.Bill)
async def callbacks_get_bill(query: types.CallbackQuery,
                             state: FSMContext) -> None:
    """
    A callback function to handle the selection of a bill. This function
    is triggered when a user selects a bill from the list of available
    bills.

    :param query: The query object representing the button press.
    :type query: types.CallbackQuery
    :param state: The current state of the conversation.
    :type state: FSMContext
    :return: None
    """
    await query.message.delete()

    async with state.proxy() as data:
        data["bill"] = query.data

    await StateChat.next()

    await Bot.answer(message=query.message, text=QuestionText.amount)
