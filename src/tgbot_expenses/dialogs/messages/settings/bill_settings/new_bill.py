from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.states.chat_states import StateSettings


@Bot.message_handler(state=StateSettings.AddBill,
                     content_types=types.ContentType.ANY)
async def message_input_new_bill(message: types.Message,
                                 state: FSMContext) -> None:
    """
    Process of input a name new bill.
    """
    await Bot.delete_messages(chat_id=message.chat.id,
                              last_message_id=message.message_id, count=2)

    async with state.proxy() as data:
        data["account_name"] = message.text

    await StateSettings.next()

    await Bot.answer(message=message, text=QuestionText.amount)
