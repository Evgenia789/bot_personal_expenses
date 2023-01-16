import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.dialogs.commands.start import send_welcome
from src.tgbot_expenses.states.states_chat import StateChat
from src.tgbot_expenses.utils.chart_and_statistics import \
    get_statistics_and_chart


@Bot.callback_query_handler(state=StateChat.DataConfirmation)
async def callbacks_confirmation_data(query: types.CallbackQuery,
                                      state: FSMContext) -> None:
    """
    Data confirmation process
    """
    await Bot.delete_message(chat_id=query.message.chat.id,
                             message_id=query.message.message_id-1)

    if query.data == "Confirm":
        await query.message.delete()

        async with state.proxy() as data:
            database.insert_item(category_name=data["category"],
                                 bill_name=data["bill"],
                                 amount=data["amount"],
                                 initial_amount=data["initial_amount"])

        await get_statistics_and_chart(query.message)

        last_message = await Bot.answer(message=query.message,
                                        text=QuestionText.last_message)

        await asyncio.sleep(2)

        await last_message.delete()
    else:
        await send_welcome(message=query.message, state=state)

    await state.reset_state()
