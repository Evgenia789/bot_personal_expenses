import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.dialogs.commands.start import send_welcome
from src.tgbot_expenses.states.chat_states import StateChat
from src.tgbot_expenses.utils.chart_and_statistics import \
    get_statistics_and_chart


@Bot.callback_query_handler(text="confirm", state=StateChat.DataConfirmation)
async def callbacks_confirmation_data(query: types.CallbackQuery,
                                      state: FSMContext) -> None:
    """
    Data confirmation process
    """
    await Bot.delete_message(chat_id=query.message.chat.id,
                             message_id=query.message.message_id-1)

    await query.message.delete()  # Why???

    async with state.proxy() as data:
        # The category name is not None, if this is the process of confirming
        # expense data, if this is the process of confirming income data,
        # then the category name will be None
        category = data.get("category")
        if category is not None:
            database.insert_item(category_name=data["category"],
                                 bill_name=data["bill"],
                                 amount=data["amount"],
                                 initial_amount=data["initial_amount"])
        else:
            database.insert_income(bill_name=data["bill"],
                                   amount=data["amount"])

    last_message = await Bot.answer(message=query.message,
                                    text=QuestionText.last_message)

    await asyncio.sleep(2)

    if category is not None:
        await last_message.delete()
        await get_statistics_and_chart(query.message)
    else:
        await send_welcome(message=last_message, state=state)

    await state.reset_state()
