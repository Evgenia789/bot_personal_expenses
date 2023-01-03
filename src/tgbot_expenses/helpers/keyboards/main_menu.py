from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_main_menu() -> InlineKeyboardMarkup:
    """
    Generating a keyboard with main menu buttons.
    """
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="View statistics",
                             callback_data="view_statistics"),
        InlineKeyboardButton(text="Make expenses",
                             callback_data="make_expenses"),
        InlineKeyboardButton(text="Settings",
                             callback_data="settings")
    )

    return keyboard
