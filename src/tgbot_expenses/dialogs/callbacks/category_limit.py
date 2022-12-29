from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.dialogs.callbacks.start_or_continue import (
    callbacks_continue, callbacks_start_over)
from src.tgbot_expenses.helpers.keyboards.back_or_main_menu import \
    get_keyboard_back_or_main_menu
from src.tgbot_expenses.states.states_settings import StateSettings


@Bot.callback_query_handler(state=StateSettings.ChangeLimit)
async def callbacks_update_limit(query: types.CallbackQuery,
                                 state: FSMContext) -> None:
    """
    Process of changing a limit.
    """
    await query.message.delete()

    await StateSettings.NewLimit.set()

    category = query.data

    limit_category = database.get_category_limit(category_name=category)

    async with state.proxy() as data:
        data["current_category"] = category
        data["limit_category"] = limit_category

    await Bot.answer(
        query.message,
        f"Current limit: {limit_category}\nSend a new limit for category",
        reply_markup=str(get_keyboard_back_or_main_menu(main_menu_button=False))
    )
