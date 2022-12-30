from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.states.states_chat import StateChat


@Bot.callback_query_handler(state=StateChat.Bill)
async def callbacks_get_bill(query: types.CallbackQuery,
                         state: FSMContext) -> None:
    """
    The process of selecting a bill.
    """
    await query.message.delete()

    async with state.proxy() as data:
        data["bill"] = query.data

    await StateChat.next()

    await Bot.answer(message=query.message, text=QuestionText.amount)
