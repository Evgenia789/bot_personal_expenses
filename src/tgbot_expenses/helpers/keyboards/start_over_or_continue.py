from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_start_over_or_continue() -> InlineKeyboardMarkup:
    """
    Generating a keyboard with main menu buttons.
    """
    keyboard = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(text="Start over",
                             callback_data="start_over"),
        InlineKeyboardButton(text="Continue",
                             callback_data="continue")
    )

    return keyboard
