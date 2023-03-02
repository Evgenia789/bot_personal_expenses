from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_changing_category() -> InlineKeyboardMarkup:
    """
    Returns an InlineKeyboardMarkup object representing a keyboard
    for changing category options.

    Returns:
        InlineKeyboardMarkup: An InlineKeyboardMarkup object representing
                              the generated keyboard.

    Examples:
        To generate a keyboard for changing catrgory options, use:
        >>> keyboard = get_keyboard_changing_category()
    """
    keyboard = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(text="Add category",
                             callback_data="add_category"),
        InlineKeyboardButton(text="Delete category",
                             callback_data="delete_category"),
        InlineKeyboardButton(text="Back", callback_data="back")
    )

    return keyboard
