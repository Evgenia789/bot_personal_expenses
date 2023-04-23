from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.dialogs.messages.expenses.empty_data import \
    message_empty_data
from src.tgbot_expenses.helpers.keyboards.question import get_keyboard_question
from src.tgbot_expenses.states.chat_states import StateChat, StateEmpty
from src.tgbot_expenses.utils.queries_database import \
    get_all_accounts_with_retry


@Bot.callback_query_handler(state=StateChat.Category)
async def callbacks_get_category(query: types.CallbackQuery,
                                 state: FSMContext) -> None:
    """
    A callback function to handle the selection of a category. This function
    is triggered when a user selects a category from the list of available
    categories.

    :param query: The query object representing the button press.
    :type query: types.CallbackQuery
    :param state: The current state of the conversation.
    :type state: FSMContext
    :return: None
    """
    await query.message.delete()

    accounts = await get_all_accounts_with_retry(
        telegram_id=query.from_user.id
    )

    if not accounts:
        await StateEmpty.InvalidEmpty.set()
        await message_empty_data(message=query.message, state=state)

    async with state.proxy() as data:
        data["category"] = query.data

    await StateChat.next()

    await Bot.answer(
        message=query.message,
        text=QuestionText.account,
        reply_markup=get_keyboard_question(
            button_names=accounts
        )
    )
