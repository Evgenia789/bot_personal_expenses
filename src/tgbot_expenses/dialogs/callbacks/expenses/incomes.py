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


@Bot.callback_query_handler(text="make_incomes", state=StateChat.MainMenu)
async def callbacks_make_incomes(query: types.CallbackQuery,
                                 state: FSMContext) -> None:
    """
    Handles the 'Make incomes' button press in the main menu,
    allowing the user to make incomes.

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

    await StateChat.Account.set()

    await Bot.answer(
        message=query.message,
        text=QuestionText.account,
        reply_markup=get_keyboard_question(
            button_names=accounts,
            button_back=True
        )
    )
