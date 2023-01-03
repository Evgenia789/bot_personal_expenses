import aiogram
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.helpers.keyboards.main_menu import \
    get_keyboard_main_menu
from src.tgbot_expenses.states.states_chat import StateChat


@Bot.message_handler(commands=["start"], state="*")
async def send_welcome(message: aiogram.types.Message,
                       state: FSMContext) -> None:
    """
    Start command handler
    """
    await message.delete()

    await StateChat.MainMenu.set()

    await Bot.answer(
        message=message,
        text=QuestionText.main_menu,
        reply_markup=str(get_keyboard_main_menu())
    )
