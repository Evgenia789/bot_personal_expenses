from decimal import Decimal, InvalidOperation

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.dialogs.messages.invalid_amount import \
    message_invalid_amount
from src.tgbot_expenses.helpers.keyboards.question import get_keyboard_question
from src.tgbot_expenses.states.chat_states import (StateCurrencyExchange,
                                                   StateInvalid)
from src.tgbot_expenses.utils.queries_database import \
    get_all_accounts_with_retry


@Bot.message_handler(state=StateCurrencyExchange.FromAccountAmount,
                     content_types=types.ContentType.ANY)
async def message_amount(message: types.Message, state: FSMContext) -> None:
    """
    Processes the user's message about the amount entered for the account
    from which the money is being converted.

    :param message: The Message object containing the user's input message.
    :type message: types.Message
    :param state: The FSMContext object representing the current state
                  of the chat.
    :type state: FSMContext
    :return: None
    """
    await Bot.delete_messages(chat_id=message.chat.id,
                              last_message_id=message.message_id, count=2)

    try:
        amount = Decimal(message.text.replace(",", "."))
    except (ValueError, InvalidOperation):
        async with state.proxy() as data:
            data["previous_question"] = QuestionText.amount
            data["state"] = state.get_state()

        await StateInvalid.InvalidAmount.set()
        await message_invalid_amount(message=message, state=state)
    else:
        async with state.proxy() as data:
            data["amount_old_currency"] = round(amount, 2)

        await StateCurrencyExchange.next()

        accounts = await get_all_accounts_with_retry(
            telegram_id=message.from_user.id
        )
        await Bot.answer(
            message=message,
            text=QuestionText.to_account,
            reply_markup=get_keyboard_question(
                button_names=accounts,
                button_back=True
            )
        )
