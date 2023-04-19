from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.helpers.keyboards.question import get_keyboard_question
from src.tgbot_expenses.states.chat_states import StateSettings
from src.tgbot_expenses.utils.queries_database import \
    get_all_accounts_with_retry


@Bot.callback_query_handler(text="delete_account",
                            state=StateSettings.ChangeAccount)
async def callbacks_get_account_for_deletting(query: types.CallbackQuery,
                                              state: FSMContext) -> None:
    """
    Handles the 'Delete account' button press in the account change menu,
    allowing the user to delete an account to the list.

    :param query: The query object representing the button press.
    :type query: types.CallbackQuery
    :param state: The current state of the conversation.
    :type state: FSMContext
    :return: None
    """
    await query.message.delete()

    await StateSettings.DeleteAccount.set()

    accounts = await get_all_accounts_with_retry(
        telegram_id=query.from_user.id
    )
    await Bot.answer(
        message=query.message,
        text=QuestionText.archive_account,
        reply_markup=str(get_keyboard_question(
            accounts,
            button_back=True
        ))
    )
