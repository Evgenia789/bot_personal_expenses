from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import ButtonText, QuestionText
from src.tgbot_expenses.dialogs.messages.invalid_amount import \
    message_invalid_amount
from src.tgbot_expenses.helpers.keyboards.question import get_keyboard_question
from src.tgbot_expenses.states.states_chat import StateChat


@Bot.message_handler(state=StateChat.Amount,
                     content_types=types.ContentType.ANY)
async def message_amount(message: types.Message, state: FSMContext) -> None:
    """
    Process a message about the amount of expenses.
    """
    await Bot.delete_messages(chat_id=message.chat.id,
                              last_message_id=message.message_id, count=2)

    if not message.text.isdigit():
        await StateChat.next()
        await message_invalid_amount(message=message, state=state)
    else:
        async with state.proxy() as data:
            data["amount"] = int(message.text)
            category = data["category"]
            bill = data["bill"]
            amount = data["amount"]

        await StateChat.DataConfirmation.set()

        await Bot.answer(message=message,
                         text=(
                            f"<b>Category:</b> {category} \n"
                            f"<b>Bill:</b> {bill}\n"
                            f"<b>Amount:</b> {amount}\n\n"
                         ) + QuestionText.confirmation,
                         reply_markup=get_keyboard_question(
                            button_names=ButtonText.confirmation
                         ))
