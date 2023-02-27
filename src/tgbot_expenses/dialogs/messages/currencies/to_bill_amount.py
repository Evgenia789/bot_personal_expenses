from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.dialogs.messages.invalid_amount import \
    message_invalid_amount
from src.tgbot_expenses.states.chat_states import (StateCurrencyExchange,
                                                   StateInvalid)
from src.tgbot_expenses.helpers.keyboards.confirmation import \
    get_keyboard_confirmation


@Bot.message_handler(state=StateCurrencyExchange.ToBillAmount,
                     content_types=types.ContentType.ANY)
async def message_amount(message: types.Message, state: FSMContext) -> None:
    """
    Process a message about the amount.
    """
    await Bot.delete_messages(chat_id=message.chat.id,
                              last_message_id=message.message_id, count=2)

    try:
        amount = float(message.text.replace(",", "."))
    except ValueError:
        async with state.proxy() as data:
            data["previous_question"] = QuestionText.amount
            data["state"] = await state.get_state()

        await StateInvalid.InvalidAmount.set()
        await message_invalid_amount(message=message, state=state)
    else:
        async with state.proxy() as data:
            bill_from = data["bill_from"]
            amount_old_currency = data["amount_old_currency"]
            bill_to = data["bill_to"]
            data["currency_amount"] = round(amount, 2)

        await StateCurrencyExchange.next()

        text_message = (f"<b>The bill to transfer money from:</b> {bill_from}\n"
                    f"<b>Amount:</b> {amount_old_currency}\n"
                    f"<b>The bill to transfer money to:</b> {bill_to}\n"
                    f"<b>Amount:</b> {amount}\n"
                    ) + QuestionText.confirmation

        await Bot.answer(message=message,
                        text=text_message,
                        reply_markup=get_keyboard_confirmation())
