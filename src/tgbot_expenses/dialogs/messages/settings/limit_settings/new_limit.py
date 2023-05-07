from decimal import Decimal, InvalidOperation

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.dialogs.messages.invalid_amount import \
    message_invalid_amount
from src.tgbot_expenses.dialogs.messages.settings.beginning import \
    go_back_to_main_menu
from src.tgbot_expenses.services.category_service import update_monthly_limit
from src.tgbot_expenses.states.chat_states import StateInvalid, StateSettings


@Bot.message_handler(state=StateSettings.NewLimit,
                     content_types=types.ContentType.ANY)
async def message_set_new_limit(message: types.Message,
                                state: FSMContext) -> None:
    """
    Handles the user input for setting a new limit for a category.

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
            data["previous_question"] = QuestionText.category_limit
            data["state"] = await state.get_state()

        await StateInvalid.InvalidAmount.set()

        await message_invalid_amount(message, state)
    else:
        async with state.proxy() as data:
            current_category = data["current_category"]

        await update_monthly_limit(category_name=current_category,
                                   new_limit=message.text,
                                   telegram_id=message.from_user.id)

        last_message = await Bot.answer(
            message=message,
            text=(f"Limit updated. Category: {current_category} \n"
                  f"New limit: {limit}")
        )

        await go_back_to_main_menu(message=last_message, state=state)
