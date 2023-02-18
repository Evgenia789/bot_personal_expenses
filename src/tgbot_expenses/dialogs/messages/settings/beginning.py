import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.dialogs.commands.start import send_welcome


async def go_back_to_main_menu(message: types.Message,
                               state: FSMContext):
    """Go back to the main menu"""
    await asyncio.sleep(2)

    await state.reset_data()

    await send_welcome(message=message, state=state)
