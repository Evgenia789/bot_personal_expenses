import aiogram
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.helpers.keyboards.main_menu import \
    get_keyboard_main_menu
from src.tgbot_expenses.services.user_service import insert_user
from src.tgbot_expenses.states.chat_states import StateChat


@Bot.message_handler(commands=["init"], state="*")
async def initialization(message: aiogram.types.Message,
                         state: FSMContext) -> None:
    """
    The process of processing the /init command.
    :param message: The Message object representing the /init command.
    :type message: aiogram.types.Message
    :param state: The FSMContext object representing the current state
                  of the chat.
    :type state: FSMContext
    :return: None
    """
    await Bot.delete_messages(chat_id=message.chat.id,
                              last_message_id=message.message_id,
                              count=2)

    await insert_user(telegram_id=message.from_user.id)

    await StateChat.MainMenu.set()

    await Bot.answer(
        message=message,
        text=QuestionText.main_menu,
        reply_markup=str(get_keyboard_main_menu())
    )
