from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.states.chat_states import StateChat


@Bot.callback_query_handler(state=StateChat.Account)
async def callbacks_get_account(query: types.CallbackQuery,
                                state: FSMContext) -> None:
    """
    A callback function to handle the selection of an account. This function
    is triggered when a user selects an account from the list of available
    accounts.

    :param query: The query object representing the button press.
    :type query: types.CallbackQuery
    :param state: The current state of the conversation.
    :type state: FSMContext
    :return: None
    """
    await query.message.delete()

    async with state.proxy() as data:
        data["account"] = query.data

    await StateChat.next()

    await Bot.answer(message=query.message, text=QuestionText.amount)
