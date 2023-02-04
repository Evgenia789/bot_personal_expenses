from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_settings() -> InlineKeyboardMarkup:
    """
    Generating a keyboard with settings buttons.
    """
    keyboard = InlineKeyboardMarkup(row_width=3).add(
        InlineKeyboardButton(text="Change limit",
                             callback_data="change_limit"),
        InlineKeyboardButton(text="Change bill",
                             callback_data="change_bill"),
        InlineKeyboardButton(text="Change category",
                             callback_data="change_category"),
        InlineKeyboardButton(text="Go back to the main menu",
                             callback_data="start_over")
    )

    return keyboard
