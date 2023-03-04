from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.helpers.keyboards.back_or_main_menu import \
    get_keyboard_back_or_main_menu
from src.tgbot_expenses.states.chat_states import StateChat
from src.tgbot_expenses.utils.message_currency_exchange_rates import \
    get_message_currency_exchange_rates


@Bot.callback_query_handler(text="currency_rates", state=StateChat.MainMenu)
async def callbacks_currency_rates(query: types.CallbackQuery,
                                   state: FSMContext) -> None:
    """
    Handles the 'Currency rates' button press in the main menu, displaying
    current currency exchange rates to the user.

    :param query: The query object representing the button press.
    :type query: types.CallbackQuery
    :param state: The current state of the conversation.
    :type state: FSMContext
    :return: None
    """
    await query.message.delete()

    text_message = await get_message_currency_exchange_rates()

    await Bot.answer(
        message=query.message,
        text=text_message,
        reply_markup=str(get_keyboard_back_or_main_menu(back_button=False))
    )
