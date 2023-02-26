from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.states.chat_states import StateCurrencyExchange


@Bot.callback_query_handler(state=StateCurrencyExchange.FromBill)
async def callbacks_get_bill_from(query: types.CallbackQuery,
                                  state: FSMContext) -> None:
    """
    The process of selecting a bill.
    """
    await query.message.delete()

    async with state.proxy() as data:
        data["bill_from"] = query.data

    await StateCurrencyExchange.next()

    await Bot.answer(message=query.message, text=QuestionText.amount)
