from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_settings() -> InlineKeyboardMarkup:
    """
    Returns an InlineKeyboardMarkup object representing a settings menu
    with customizable buttons.

    The generated keyboard has buttons for changing the category's limit,
    account, and category, as well as a "Go back to the main menu" button.

    Example:

        To generate a settings menu keyboard:

        .. code-block:: python3

            keyboard = get_keyboard_settings()

    :return: InlineKeyboardMarkup
    """
    keyboard = InlineKeyboardMarkup(row_width=3).add(
        InlineKeyboardButton(text="Change limit",
                             callback_data="change_limit"),
        InlineKeyboardButton(text="Change account",
                             callback_data="change_account"),
        InlineKeyboardButton(text="Change category",
                             callback_data="change_category"),
        InlineKeyboardButton(text="Go back to the main menu",
                             callback_data="start_over")
    )

    return keyboard
