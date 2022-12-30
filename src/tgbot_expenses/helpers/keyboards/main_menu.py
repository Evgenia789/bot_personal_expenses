from aiogram import types


def get_keyboard_main_menu() -> types.InlineKeyboardMarkup:
    """
    Generating a keyboard with main menu buttons.
    """
    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(
            text="View statistics",
            callback_data="view_statistics"),
        types.InlineKeyboardButton(
            text="Make expenses",
            callback_data="make_expenses"),
        types.InlineKeyboardButton(
            text="Settings",
            callback_data="settings")
    )

    return keyboard
