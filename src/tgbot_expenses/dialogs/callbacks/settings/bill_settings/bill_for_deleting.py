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
    The process of selecting a bill to delete.
    """
    await query.message.delete()

    await StateSettings.DeleteBill.set()

    await Bot.answer(
        message=query.message,
        text=QuestionText.archive_bill,
        reply_markup=str(get_keyboard_question(
            database.get_all_bills(),
            button_back=True
        ))
    )
