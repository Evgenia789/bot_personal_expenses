from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.helpers.keyboards.changing_category import \
    get_keyboard_changing_category
from src.tgbot_expenses.states.states_settings import StateSettings


@Bot.callback_query_handler(text="change_category",
                            state=StateSettings.MainMenu)
async def callbacks_change_category(query: types.CallbackQuery,
                                    state: FSMContext) -> None:
    """
    The process of changing the category.
    """
    await query.message.delete()

    await StateSettings.ChangeCategory.set()

    await Bot.answer(
        message=query.message,
        text=QuestionText.changing,
        reply_markup=str(get_keyboard_changing_category())
    )
