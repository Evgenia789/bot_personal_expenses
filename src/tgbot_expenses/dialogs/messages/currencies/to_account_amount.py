from decimal import Decimal, InvalidOperation

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.dialogs.messages.invalid_amount import \
    message_invalid_amount
from src.tgbot_expenses.helpers.keyboards.confirmation import \
    get_keyboard_confirmation
from src.tgbot_expenses.states.chat_states import (StateCurrencyExchange,
                                                   StateInvalid)


@Bot.message_handler(state=StateCurrencyExchange.ToAccountAmount,
                     content_types=types.ContentType.ANY)
async def message_amount(message: types.Message, state: FSMContext) -> None:
    """
    Processes the user's message about the amount entered for the account
    to which the money is being converted

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
            data["state"] = await state.get_state()

        await StateInvalid.InvalidAmount.set()
        await message_invalid_amount(message=message, state=state)
    else:
        async with state.proxy() as data:
            account_from = data["account_from"]
            amount_old_currency = data["amount_old_currency"]
            account_to = data["account_to"]
            data["currency_amount"] = round(amount, 2)

        await StateCurrencyExchange.next()

        text_message = (
            f"<b>The account to transfer money from:</b> {account_from}\n"
            f"<b>Amount:</b> {amount_old_currency}\n"
            f"<b>The account to transfer money to:</b> {account_to}\n"
            f"<b>Amount:</b> {amount}\n"
        ) + QuestionText.confirmation

        await Bot.answer(message=message,
                         text=text_message,
                         reply_markup=get_keyboard_confirmation())
