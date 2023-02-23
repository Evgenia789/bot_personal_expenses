from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.dialogs.commands.start import send_welcome
from src.tgbot_expenses.states.chat_states import StateChat


@Bot.callback_query_handler(text="cancel", state=StateChat.DataConfirmation)
async def callbacks_confirmation_data(query: types.CallbackQuery,
                                      state: FSMContext) -> None:
    """
    Cancel process
    """
    await Bot.delete_message(chat_id=query.message.chat.id,
                             message_id=query.message.message_id-1)

    await send_welcome(message=query.message, state=state)

    await state.reset_state()
