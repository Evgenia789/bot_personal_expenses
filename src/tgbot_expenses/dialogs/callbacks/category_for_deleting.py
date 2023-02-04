from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.helpers.keyboards.question import get_keyboard_question
from src.tgbot_expenses.states.states_settings import StateSettings


@Bot.callback_query_handler(text="delete_category",
                            state=StateSettings.ChangeCategory)
async def callbacks_get_category_for_deleting(query: types.CallbackQuery,
                                              state: FSMContext) -> None:
    """
    The process of selecting a category to delete.
    """
    await query.message.delete()

    await StateSettings.DeleteCategory.set()

    await Bot.answer(
        message=query.message,
        text=QuestionText.archive_category,
        reply_markup=str(get_keyboard_question(
            database.get_all_categories(),
            button_back=True
        ))
    )
