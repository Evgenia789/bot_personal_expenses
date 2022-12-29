from aiogram import types


def get_keyboard_settings() -> types.InlineKeyboardMarkup:
    """
    Generating a keyboard with settings buttons.
    """
    keyboard = types.InlineKeyboardMarkup(row_width=2).add(
        types.InlineKeyboardButton(
            text="Change limit",
            callback_data="change_limit"),
        types.InlineKeyboardButton(
            text="Change bill",
            callback_data="change_bill"),
        types.InlineKeyboardButton(
            text="Go back to the main menu",
            callback_data="start_over")    
    )

    return keyboard
