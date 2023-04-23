from aiogram import types

from src.tgbot_expenses.helpers.keyboards.back_or_main_menu import \
    get_keyboard_back_or_main_menu
from src.tgbot_expenses.services.expense_service import get_monthly_expenses
from src.tgbot_expenses.utils.expense_chart import get_chart
from src.tgbot_expenses.utils.text_statistics import get_data


async def get_statistics_and_chart(message: types.Message,
                                   telegram_id: int) -> types.Message:
    """
    Retrieve monthly expense data from the database, generate a chart
    and a message containing the data, and send them to the user.

    :param message: The message triggering the function.
    :type message: types.Message
    :return: types.Message
    """
    monthly_expense_data = await get_monthly_expenses(
        telegram_id=telegram_id
    )

    text_message = await get_data(data=monthly_expense_data)
    path_to_chart = await get_chart(data=monthly_expense_data)

    message = await message.answer_photo(
        photo=types.InputFile(path_or_bytesio=path_to_chart),
        caption=text_message,
        reply_markup=str(get_keyboard_back_or_main_menu(back_button=False))
    )

    return message
