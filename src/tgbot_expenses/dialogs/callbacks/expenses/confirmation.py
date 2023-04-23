import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.dialogs.commands.start import send_welcome
from src.tgbot_expenses.services.expense_service import insert_expense
from src.tgbot_expenses.services.income_service import insert_income
from src.tgbot_expenses.states.chat_states import StateChat
from src.tgbot_expenses.utils.chart_and_statistics import \
    get_statistics_and_chart


@Bot.callback_query_handler(text="confirm", state=StateChat.DataConfirmation)
async def callbacks_confirmation_data(query: types.CallbackQuery,
                                      state: FSMContext) -> None:
    """
    A callback function to handle the confirmation of a data confirmation
    process. This function is triggered when a user selects the "Confirm"
    option during the confirmation process.

    :param query: The query object representing the button press.
    :type query: types.CallbackQuery
    :param state: The current state of the conversation.
    :type state: FSMContext
    :return: None
    """
    await Bot.delete_messages(chat_id=query.message.chat.id,
                              last_message_id=query.message.message_id,
                              count=2)

    async with state.proxy() as data:
        # The category name is not None, if this is the process of confirming
        # expense data, if this is the process of confirming income data,
        # then the category name will be None
        category = data.get("category")
        if category is not None:
            await insert_expense(category_name=data["category"],
                                 account_name=data["account"],
                                 amount=data["amount"],
                                 telegram_id=query.from_user.id)
        else:
            await insert_income(account_name=data["account"],
                                amount=data["amount"],
                                telegram_id=query.from_user.id)

    last_message = await Bot.answer(message=query.message,
                                    text=QuestionText.last_message)

    await asyncio.sleep(2)

    if category is not None:
        await last_message.delete()
        await get_statistics_and_chart(query.message,
                                       telegram_id=query.from_user.id)
    else:
        await send_welcome(message=last_message, state=state)

    await state.reset_state()
