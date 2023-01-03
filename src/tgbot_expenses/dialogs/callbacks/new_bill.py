from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.helpers.keyboards.back_or_main_menu import \
    get_keyboard_back_or_main_menu
from src.tgbot_expenses.states.states_settings import StateSettings


@Bot.callback_query_handler(text="add_bill", state=StateSettings.ChangeBill)
async def callbacks_add_new_bill(query: types.CallbackQuery,
                                 state: FSMContext) -> None:
    """
    The process of adding a new bill.
    """
    await query.message.delete()

    await StateSettings.AddBill.set()

    await Bot.answer(
        message=query.message,
        text=QuestionText.new_bill,
        reply_markup=str(get_keyboard_back_or_main_menu(
            main_menu_button=False
        ))
    )
