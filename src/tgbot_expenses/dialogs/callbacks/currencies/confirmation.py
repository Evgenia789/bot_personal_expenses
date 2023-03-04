import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.dialogs.commands.start import send_welcome
from src.tgbot_expenses.states.chat_states import StateCurrencyExchange


@Bot.callback_query_handler(text="confirm",
                            state=StateCurrencyExchange.DataConfirmation)
async def callbacks_confirmation_data(query: types.CallbackQuery,
                                      state: FSMContext) -> None:
    """
    A callback function to handle the confirmation of a data confirmation
    process. This function is triggered when a user selects the "Confirm"
    option during the confirmation process.

    :param query: The query object representing the button press.
    :type query: types.CallbackQuery
    :param state: The current state of the conversation.
    :type state: FSMContext
    :return: None
    """
    await Bot.delete_messages(chat_id=query.message.chat.id,
                              last_message_id=query.message.message_id,
                              count=2)

    async with state.proxy() as data:
        database.update_amount(bill_from=data["bill_from"],
                               amount_old_currency=data["amount_old_currency"],
                               currency_amount=data["currency_amount"],
                               bill_to=data["bill_to"])

    last_message = await Bot.answer(message=query.message,
                                    text=QuestionText.last_message)

    await asyncio.sleep(2)

    await send_welcome(message=last_message, state=state)

    await state.reset_state()
