from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_changing_bill() -> InlineKeyboardMarkup:
    """
    Generating a keyboard with changing bill buttons.
    """
    keyboard = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(text="Add bill",
                             callback_data="add_bill"),
        InlineKeyboardButton(text="Delete bill",
                             callback_data="delete_bill"),
        InlineKeyboardButton(text="Back", callback_data="back")
    )

    return keyboard
