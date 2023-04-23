from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.helpers.keyboards.question import get_keyboard_question
from src.tgbot_expenses.states.chat_states import StateSettings
from src.tgbot_expenses.utils.queries_database import \
    get_all_categories_with_retry


@Bot.callback_query_handler(text="delete_category",
                            state=StateSettings.ChangeCategory)
async def callbacks_get_category_for_deleting(query: types.CallbackQuery,
                                              state: FSMContext) -> None:
    """
    Handles the 'Delete category' button press in the category change menu,
    allowing the user to delete a category to the list.

    :param query: The query object representing the button press.
    :type query: types.CallbackQuery
    :param state: The current state of the conversation.
    :type state: FSMContext
    :return: None
    """
    await query.message.delete()

    await StateSettings.DeleteCategory.set()

    categories = await get_all_categories_with_retry(
        telegram_id=query.from_user.id
    )
    await Bot.answer(
        message=query.message,
        text=QuestionText.archive_category,
        reply_markup=str(get_keyboard_question(
            categories,
            button_back=True
        ))
    )
