from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.dialogs.messages.invalid_amount import \
    message_invalid_amount
from src.tgbot_expenses.helpers.keyboards.question import get_keyboard_question
from src.tgbot_expenses.states.chat_states import (StateCurrencyExchange,
                                                   StateInvalid)
from src.tgbot_expenses.utils.dollar_amount import get_dollar_amount


@Bot.message_handler(state=StateCurrencyExchange.Amount,
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
            data["amount_old_currency"] = round(amount, 2)
            data["dollar_amount"] = await get_dollar_amount(
                bill=data["bill_from"],
                amount=amount
            )

        await StateCurrencyExchange.next()

        await Bot.answer(
            message=message,
            text=QuestionText.to_bill,
            reply_markup=get_keyboard_question(
                button_names=database.get_all_bills(),
                button_back=True
            )
        )
