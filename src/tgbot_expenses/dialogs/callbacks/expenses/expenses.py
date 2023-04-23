from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.dialogs.messages.expenses.empty_data import \
    message_empty_data
from src.tgbot_expenses.helpers.keyboards.question import get_keyboard_question
from src.tgbot_expenses.states.chat_states import StateChat, StateEmpty
from src.tgbot_expenses.utils.queries_database import \
    get_all_categories_with_retry


@Bot.callback_query_handler(text="make_expenses", state=StateChat.MainMenu)
async def callbacks_make_expenses(query: types.CallbackQuery,
                                  state: FSMContext) -> None:
    """
    Handles the 'Make expenses' button press in the main menu,
    allowing the user to make expenses.

    :param query: The query object representing the button press.
    :type query: types.CallbackQuery
    :param state: The current state of the conversation.
    :type state: FSMContext
    :return: None
    """
    await query.message.delete()

    categories = await get_all_categories_with_retry(
        telegram_id=query.from_user.id
    )

    if not categories:
        await StateEmpty.InvalidEmpty.set()
        await message_empty_data(message=query.message, state=state)

    await StateChat.Category.set()

    await Bot.answer(
        message=query.message,
        text=QuestionText.category,
        reply_markup=get_keyboard_question(
            button_names=categories,
            button_back=True
        )
    )
