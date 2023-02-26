from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.helpers.keyboards.confirmation import \
    get_keyboard_confirmation
from src.tgbot_expenses.states.chat_states import StateCurrencyExchange
from src.tgbot_expenses.utils.currency_amount import get_new_amount_currency


@Bot.callback_query_handler(state=StateCurrencyExchange.ToBill)
async def callbacks_get_bill_to(query: types.CallbackQuery,
                                state: FSMContext) -> None:
    """
    The process of selecting a bill.
    """
    await query.message.delete()

    async with state.proxy() as data:
        data["bill_to"] = query.data
        bill_from = data["bill_from"]
        amount_old_currency = data["amount_old_currency"]
        dollar_amount = data["dollar_amount"]
        data["currency_amount"] = await get_new_amount_currency(
            bill=query.data,
            dollar_amount=dollar_amount
        )

    await StateCurrencyExchange.next()

    text_message = (f"<b>The bill to transfer money from:</b> {bill_from}\n"
                    f"<b>Amount:</b> {amount_old_currency}\n"
                    f"<b>The bill to transfer money to:</b> {query.data}\n\n"
                    ) + QuestionText.confirmation

    await Bot.answer(message=query.message,
                     text=text_message,
                     reply_markup=get_keyboard_confirmation())
