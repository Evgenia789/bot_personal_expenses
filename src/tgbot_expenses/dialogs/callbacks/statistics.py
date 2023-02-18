from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.states.chat_states import StateChat
from src.tgbot_expenses.utils.chart_and_statistics import \
    get_statistics_and_chart


@Bot.callback_query_handler(text="view_statistics", state=StateChat.MainMenu)
async def callbacks_view_statistics(query: types.CallbackQuery,
                                    state: FSMContext) -> None:
    """
    The process of displaying statistics.
    """
    await query.message.delete()

    await get_statistics_and_chart(query.message)
