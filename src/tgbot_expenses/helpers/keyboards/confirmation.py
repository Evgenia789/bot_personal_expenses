from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_confirmation() -> InlineKeyboardMarkup:
    """
    Generating a keyboard with confirmation buttons.
    """
    keyboard = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(text="Confirm",
                             callback_data="confirm"),
        InlineKeyboardButton(text="Cancel",
                             callback_data="cancel")
    )

    return keyboard
