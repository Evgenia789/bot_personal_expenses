from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.helpers.keyboards.main_menu import \
    get_keyboard_main_menu
from src.tgbot_expenses.states.states_chat import StateChat


@Bot.callback_query_handler(text="start_over", state="*")
async def callbacks_start_over(query: types.CallbackQuery,
                              state: FSMContext) -> None:
    """
    Process start over button
    """
    await query.message.delete()
    # await query.message.delete()

    await state.reset_data()

    await StateChat.MainMenu.set()

    await Bot.answer(
        query.message,
        QuestionText.main_menu,
        reply_markup=str(get_keyboard_main_menu())
    )


@Bot.callback_query_handler(text="continue", state="*")
async def callbacks_continue(query: types.CallbackQuery,
                             state: FSMContext) -> None:
    """
    Process continue button
    """
    await query.message.delete()
