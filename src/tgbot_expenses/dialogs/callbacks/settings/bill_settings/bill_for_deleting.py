from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.helpers.keyboards.question import get_keyboard_question
from src.tgbot_expenses.states.chat_states import StateSettings


@Bot.callback_query_handler(text="delete_bill", state=StateSettings.ChangeBill)
async def callbacks_get_bill_for_deletting(query: types.CallbackQuery,
                                           state: FSMContext) -> None:
    """
    Handles the 'Delete bill' button press in the bill change menu,
    allowing the user to delete a bill to the list.

    :param query: The query object representing the button press.
    :type query: types.CallbackQuery
    :param state: The current state of the conversation.
    :type state: FSMContext
    :return: None
    """
    await query.message.delete()

    await StateSettings.DeleteBill.set()

    accounts = await database.get_all_accounts()
    await Bot.answer(
        message=query.message,
        text=QuestionText.archive_bill,
        reply_markup=str(get_keyboard_question(
            accounts,
            button_back=True
        ))
    )
