import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.helpers.keyboards.back_or_main_menu import \
    get_keyboard_back_or_main_menu
from src.tgbot_expenses.states.states_chat import StateChat
from src.tgbot_expenses.states.states_settings import StateSettings


@Bot.message_handler(state=[StateChat.InvalidAmount,
                            StateSettings.InvalidAmount],
                     content_types=types.ContentType.ANY)
async def message_invalid_amount(message: types.Message, state: FSMContext) -> None:
    """
    Process a message about an invalid expense amount format.
    """
    message_warning = await message.answer(QuestionText.warning_number)

    current_state = await Bot.get_current_state()
    current_state_name = current_state.split(":")[0]

    await asyncio.sleep(2)

    await message_warning.delete()

    if current_state_name == "StateChat":
        await StateChat.Amount.set()

        await Bot.answer(message=message, text=QuestionText.amount)
    else:
        await StateSettings.NewLimit.set()

        async with state.proxy() as data:
            limit_category = data["limit_category"]

        await Bot.answer(
            message=message,
            text=(f"Current limit: {limit_category}\n"
                  "Send a new limit for category"),
            reply_markup=str(get_keyboard_back_or_main_menu(
                main_menu_button=False
            ))
        )
    
