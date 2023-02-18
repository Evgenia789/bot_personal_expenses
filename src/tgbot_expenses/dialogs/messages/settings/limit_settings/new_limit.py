from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.dialogs.messages.invalid_amount import \
    message_invalid_amount
from src.tgbot_expenses.dialogs.messages.settings.beginning import \
    go_back_to_main_menu
from src.tgbot_expenses.states.chat_states import StateInvalid, StateSettings


@Bot.message_handler(state=StateSettings.NewLimit,
                     content_types=types.ContentType.ANY)
async def message_set_new_limit(message: types.Message,
                                state: FSMContext) -> None:
    """
    Process of setting new limit.
    """
    await Bot.delete_messages(chat_id=message.chat.id,
                              last_message_id=message.message_id, count=2)

    try:
        limit = float(message.text.replace(",", "."))
    except ValueError:
        async with state.proxy() as data:
            data["previous_question"] = QuestionText.category_limit
            data["state"] = await state.get_state()

        await StateInvalid.InvalidAmount.set()

        await message_invalid_amount(message, state)
    else:
        async with state.proxy() as data:
            current_category = data["current_category"]

        database.update_limit(category_name=current_category,
                              new_limit=message.text)

        last_message = await Bot.answer(
            message=message,
            text=(f"Limit updated. Category: {current_category} \n"
                  f"New limit: {limit}")
        )

        await go_back_to_main_menu(message=last_message, state=state)
