from aiogram import types


def get_keyboard_start_over_or_continue() -> types.InlineKeyboardMarkup:
    """
    Generating a keyboard with main menu buttons.
    """
    keyboard = types.InlineKeyboardMarkup(row_width=2).add(
        types.InlineKeyboardButton(
            text="Start over",
            callback_data="start_over"),
        types.InlineKeyboardButton(
            text="Continue",
            callback_data="continue")
    )

    return keyboard
