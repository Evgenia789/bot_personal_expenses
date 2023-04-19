import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.dialogs.commands.start import send_welcome
from src.tgbot_expenses.services.account_service import archive_account
from src.tgbot_expenses.states.chat_states import StateSettings


@Bot.callback_query_handler(state=StateSettings.DeleteAccount)
async def callbacks_delete_account(query: types.CallbackQuery,
                                   state: FSMContext) -> None:
    """
    Handles the button press for deleting an account.

    :param query: The query object representing the button press.
    :type query: types.CallbackQuery
    :param state: The current state of the conversation.
    :type state: FSMContext
    :return: None
    """
    await query.message.delete()

    await StateSettings.next()

    await archive_account(account_name=query.data,
                          telegram_id=query.from_user.id)

    last_message = await Bot.answer(
        message=query.message,
        text=QuestionText.result_archive
    )

    await asyncio.sleep(2)

    await send_welcome(message=last_message, state=state)
