from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_settings() -> InlineKeyboardMarkup:
    """
    Returns an InlineKeyboardMarkup object representing a settings menu
    with customizable buttons.

    The generated keyboard has buttons for changing the user's limit, bill,
    and category, as well as a "Go back to the main menu" button.

    Returns:
        InlineKeyboardMarkup: An InlineKeyboardMarkup object representing
                              the generated keyboard.

    Examples:
        To generate a settings menu keyboard, use:
        >>> keyboard = get_keyboard_settings()
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
