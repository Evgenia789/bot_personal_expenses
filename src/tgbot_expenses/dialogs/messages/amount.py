from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import ButtonText, QuestionText
from src.tgbot_expenses.dialogs.callbacks.start_or_continue import (
    callbacks_continue, callbacks_start_over)
from src.tgbot_expenses.dialogs.messages.invalid_amount import \
    message_invalid_amount
from src.tgbot_expenses.helpers.keyboards.question import \
    get_keyboard_question
from src.tgbot_expenses.states.states_chat import StateChat


@Bot.message_handler(state=StateChat.Amount, content_types=types.ContentType.ANY)
async def message_amount(message: types.Message, state: FSMContext) -> None:
    """
    Process a message about the amount of expenses.
    """
    await Bot.delete_messages(message.chat.id, message.message_id, 2)
    if not message.text.isdigit():
        await StateChat.next()
        await message_invalid_amount(message, state)
    else:
        async with state.proxy() as data:
            data["amount"] = int(message.text)
            category = data["category"]
            bill = data["bill"]
            amount = data["amount"]

        await StateChat.DataConfirmation.set()
        await Bot.answer(message, f"Category: {category} \nBill: {bill} \nAmount: {amount}")
        await Bot.answer(
            message,
            QuestionText.confirmation,
            reply_markup=get_keyboard_question(ButtonText.confirmation)
        )
