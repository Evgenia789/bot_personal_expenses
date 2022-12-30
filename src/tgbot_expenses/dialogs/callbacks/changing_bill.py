from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.helpers.keyboards.changing_bill import \
    get_keyboard_changing_bill
from src.tgbot_expenses.states.states_settings import StateSettings


@Bot.callback_query_handler(text="change_bill", state=StateSettings.MainMenu)
async def callbacks_change_bill(query: types.CallbackQuery,
                                state: FSMContext) -> None:
    """
    The process of changing the bill.
    """
    await query.message.delete()

    await StateSettings.ChangeBill.set()
        
    await Bot.answer(
        message=query.message,
        text=QuestionText.bills,
        reply_markup=str(get_keyboard_changing_bill())
    )
