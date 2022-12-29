from aiogram import types


def get_keyboard_changing_bill() -> types.InlineKeyboardMarkup:
    """
    Generating a keyboard with changing bill buttons.
    """
    keyboard = types.InlineKeyboardMarkup(row_width=2).add(
        types.InlineKeyboardButton(
            text="Add bill",
            callback_data="add_bill"),
        types.InlineKeyboardButton(
            text="Delete bill",
            callback_data="delete_bill"),
        types.InlineKeyboardButton(
            text="Back",
            callback_data="back")
    )

    return keyboard
