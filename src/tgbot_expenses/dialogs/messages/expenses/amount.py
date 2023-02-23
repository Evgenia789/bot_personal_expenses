from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.dialogs.messages.invalid_amount import \
    message_invalid_amount
from src.tgbot_expenses.helpers.keyboards.confirmation import \
    get_keyboard_confirmation
from src.tgbot_expenses.states.chat_states import StateChat, StateInvalid
from src.tgbot_expenses.utils.dollar_amount import get_dollar_amount


@Bot.message_handler(state=StateChat.Amount,
                     content_types=types.ContentType.ANY)
async def message_amount(message: types.Message, state: FSMContext) -> None:
    """
    Process a message about the amount.
    """
    await Bot.delete_messages(chat_id=message.chat.id,
                              last_message_id=message.message_id, count=2)

    try:
        amount = float(message.text.replace(",", "."))
    except ValueError:
        async with state.proxy() as data:
            data["previous_question"] = QuestionText.amount
            data["state"] = await state.get_state()

        await StateInvalid.InvalidAmount.set()
        await message_invalid_amount(message=message, state=state)
    else:
        async with state.proxy() as data:
            data["initial_amount"] = round(amount, 2)
            category = data.get("category")
            data["amount"] = round(amount, 2) \
                if category is None \
                else await get_dollar_amount(data["bill"], amount)
            bill = data["bill"]

        await StateChat.DataConfirmation.set()

        category_text = f"<b>Category:</b> {category} \n" \
            if category is not None else ""

        text_message = category_text + (f"<b>Bill:</b> {bill}\n"
                                        f"<b>Amount:</b> {amount}\n\n"
                                       ) + QuestionText.confirmation

        await Bot.answer(message=message,
                         text=text_message,
                         reply_markup=get_keyboard_confirmation())
