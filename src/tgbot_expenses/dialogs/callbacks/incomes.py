from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.helpers.keyboards.question import get_keyboard_question
from src.tgbot_expenses.states.states_chat import StateChat


@Bot.callback_query_handler(text="make_incomes", state=StateChat.MainMenu)
async def callbacks_make_incomes(query: types.CallbackQuery,
                                 state: FSMContext) -> None:
    """
    The process of starting to fill in incomes.
    """
    await query.message.delete()

    await StateChat.Bill.set()

    await Bot.answer(
        message=query.message,
        text=QuestionText.bill,
        reply_markup=get_keyboard_question(
            button_names=database.get_all_bills(),
            button_back=True
        )
    )
