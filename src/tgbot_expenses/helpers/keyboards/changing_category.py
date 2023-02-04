from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_changing_category() -> InlineKeyboardMarkup:
    """
    Generating a keyboard with changing category buttons.
    """
    keyboard = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(text="Add category",
                             callback_data="add_category"),
        InlineKeyboardButton(text="Delete category",
                             callback_data="delete_category"),
        InlineKeyboardButton(text="Back", callback_data="back")
    )

    return keyboard
