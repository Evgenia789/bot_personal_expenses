from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.states.states_settings import StateSettings


@Bot.message_handler(state=StateSettings.AddCategory,
                     content_types=types.ContentType.ANY)
async def message_input_new_category(message: types.Message,
                                     state: FSMContext) -> None:
    """
    Process of input a new category.
    """
    await Bot.delete_messages(chat_id=message.chat.id,
                              last_message_id=message.message_id, count=2)

    await StateSettings.next()

    async with state.proxy() as data:
        data["category_name"] = message.text

    await Bot.answer(
        message=message,
        text=QuestionText.category_limit
    )
