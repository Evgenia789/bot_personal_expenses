from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.dialogs.messages.expenses.empty_data import \
    message_empty_data
from src.tgbot_expenses.helpers.keyboards.question import get_keyboard_question
from src.tgbot_expenses.states.chat_states import (StateChat,
                                                   StateCurrencyExchange,
                                                   StateEmpty)
from src.tgbot_expenses.utils.queries_database import \
    get_all_accounts_with_retry


@Bot.callback_query_handler(text="exchange_currency", state=StateChat.MainMenu)
async def callbacks_exchange_currency(query: types.CallbackQuery,
                                      state: FSMContext) -> None:
    """
    A callback function to handle the starting of a currency exchange process.
    This function is triggered when a user selects the "Exchange currency"
    option from the main menu.

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

    await StateCurrencyExchange.FromAccount.set()

    await Bot.answer(
        message=query.message,
        text=QuestionText.from_account,
        reply_markup=get_keyboard_question(
            button_names=accounts,
            button_back=True
        )
    )
