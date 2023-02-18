from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.dialogs.messages.invalid_amount import \
    message_invalid_amount
from src.tgbot_expenses.dialogs.messages.settings.beginning import \
    go_back_to_main_menu
from src.tgbot_expenses.states.chat_states import StateInvalid, StateSettings


@Bot.message_handler(state=StateSettings.AmountBill,
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
            account_name = data["account_name"]
            database.insert_account(account_name=account_name,
                                    account_amount=amount)

        message = await Bot.answer(message=message,
                                   text=f"Account {account_name} added")

        await go_back_to_main_menu(message=message, state=state)
