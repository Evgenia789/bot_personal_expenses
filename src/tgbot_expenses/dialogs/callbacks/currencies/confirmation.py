import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.dialogs.commands.start import send_welcome
from src.tgbot_expenses.services.account_service import update_amount
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
        await update_amount(
            account_from=data["account_from"],
            amount_old_currency=data["amount_old_currency"],
            currency_amount=data["currency_amount"],
            account_to=data["account_to"],
            telegram_id=query.from_user.id
        )

    last_message = await Bot.answer(message=query.message,
                                    text=QuestionText.last_message)

    await asyncio.sleep(2)

    await send_welcome(message=last_message, state=state)

    await state.reset_state()
