from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.helpers.keyboards.back_or_main_menu import \
    get_keyboard_back_or_main_menu
from src.tgbot_expenses.states.chat_states import StateSettings


@Bot.callback_query_handler(state=StateSettings.ChangeLimit)
async def callbacks_get_category_to_change_limit(query: types.CallbackQuery,
                                                 state: FSMContext) -> None:
    """
    The process of selecting a category.
    """
    await query.message.delete()

    await StateSettings.NewLimit.set()

    limit_category = database.get_category_limit(category_name=query.data)

    async with state.proxy() as data:
        data["current_category"] = query.data
        data["limit_category"] = limit_category

    await Bot.answer(
        message=query.message,
        text=(f"Current limit: {limit_category}\n"
              "Send a new limit for category"),
        reply_markup=str(get_keyboard_back_or_main_menu(
            main_menu_button=False
        ))
    )
