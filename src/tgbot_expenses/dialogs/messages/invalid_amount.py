import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.states import chat_states


@Bot.message_handler(state=chat_states.StateInvalid.InvalidAmount,
                     content_types=types.ContentType.ANY)
async def message_invalid_amount(message: types.Message,
                                 state: FSMContext) -> None:
    """
    The process of processing an incorrectly entered message by the user.

    :param message: The Message object containing the invalid input message
                    from the user.
    :type message: types.Message
    :param state: The FSMContext object representing the current state
                  of the chat.
    :type state: FSMContext
    :return: None
    """
    await Bot.delete_message(chat_id=message.chat.id,
                             message_id=message.message_id)

    message_warning = await message.answer(QuestionText.warning_number)

    await asyncio.sleep(2)

    await message_warning.delete()

    async with state.proxy() as data:
        prev_state, state_name = data.get("state").split(":")
        text_message = data.get("previous_question")
        keyboard = data.get("reply_markup")

    await state.set_state(
        chat_states.__dict__[prev_state].__dict__[state_name]
    )

    await Bot.answer(message=message, text=text_message,
                     reply_markup=None if keyboard is None else keyboard)
