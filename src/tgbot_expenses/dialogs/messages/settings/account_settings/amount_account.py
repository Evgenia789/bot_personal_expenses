from decimal import Decimal, InvalidOperation

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.dialogs.messages.invalid_amount import \
    message_invalid_amount
from src.tgbot_expenses.dialogs.messages.settings.beginning import \
    go_back_to_main_menu
from src.tgbot_expenses.services.account_service import insert_account
from src.tgbot_expenses.states.chat_states import StateInvalid, StateSettings


@Bot.message_handler(state=StateSettings.AmountAccount,
                     content_types=types.ContentType.ANY)
async def message_amount(message: types.Message, state: FSMContext) -> None:
    """
    Processes the user's message about the amount entered for the account.

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
            account_name = data["account_name"]
            await insert_account(account_name=account_name,
                                 account_amount=amount,
                                 telegram_id=message.from_user.id)

        message = await Bot.answer(message=message,
                                   text=f"Account {account_name} added")

        await go_back_to_main_menu(message=message, state=state)
