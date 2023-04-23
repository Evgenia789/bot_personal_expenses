from decimal import Decimal, InvalidOperation

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.dialogs.messages.invalid_amount import \
    message_invalid_amount
from src.tgbot_expenses.dialogs.messages.settings.beginning import \
    go_back_to_main_menu
from src.tgbot_expenses.helpers.keyboards.back_or_main_menu import \
    get_keyboard_back_or_main_menu
from src.tgbot_expenses.services.category_service import insert_category
from src.tgbot_expenses.states.chat_states import StateInvalid, StateSettings


@Bot.message_handler(state=StateSettings.CategoryLimit,
                     content_types=types.ContentType.ANY)
async def message_input_new_category(message: types.Message,
                                     state: FSMContext) -> None:
    """
    Processes a message containing a new category limit input.

    :param message: The Message object containing the user's input message.
    :type message: types.Message
    :param state: The FSMContext object representing the current state
                  of the chat.
    :type state: FSMContext
    :return: None
    """
    await Bot.delete_messages(chat_id=message.chat.id,
                              last_message_id=message.message_id, count=2)

    try:
        limit = Decimal(message.text.replace(",", "."))
    except (ValueError, InvalidOperation):
        async with state.proxy() as data:
            data["previous_question"] = (
                f"Current limit: {data['category_name']}\n"
                "Send a new limit for category"
            )
            data["reply_markup"] = str(get_keyboard_back_or_main_menu(
                main_menu_button=False
            ))
            data["state"] = await state.get_state()

        await StateInvalid.InvalidAmount.set()

        await message_invalid_amount(message, state)
    else:
        async with state.proxy() as data:
            name_new_category = data["category_name"]

        await insert_category(category_name=name_new_category,
                              monthly_limit=limit,
                              telegram_id=message.from_user.id)

        message = await Bot.answer(
            message=message,
            text=f"Category {name_new_category} added"
        )

        await go_back_to_main_menu(message=message, state=state)
