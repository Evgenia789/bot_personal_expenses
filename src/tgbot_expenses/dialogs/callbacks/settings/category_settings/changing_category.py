from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.helpers.keyboards.changing_category import \
    get_keyboard_changing_category
from src.tgbot_expenses.states.chat_states import StateSettings


@Bot.callback_query_handler(text="change_category",
                            state=StateSettings.MainMenu)
async def callbacks_change_category(query: types.CallbackQuery,
                                    state: FSMContext) -> None:
    """
    Handles the 'Change category' button press in the settings menu,
    allowing the user to change a category to the list.

    :param query: The query object representing the button press.
    :type query: types.CallbackQuery
    :param state: The current state of the conversation.
    :type state: FSMContext
    :return: None
    """
    await query.message.delete()

    await StateSettings.ChangeCategory.set()

    await Bot.answer(
        message=query.message,
        text=QuestionText.changing,
        reply_markup=str(get_keyboard_changing_category())
    )
