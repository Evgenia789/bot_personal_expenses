from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_changing_account() -> InlineKeyboardMarkup:
    """
    Returns an InlineKeyboardMarkup object representing a keyboard
    for changing account options.

    Example:

        To generate a keyboard for changing account options:

        .. code-block:: python3

            keyboard = get_keyboard_changing_account()

    :return: InlineKeyboardMarkup
    """
    keyboard = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(text="Add account",
                             callback_data="add_account"),
        InlineKeyboardButton(text="Delete account",
                             callback_data="delete_account"),
        InlineKeyboardButton(text="Back", callback_data="back")
    )

    return keyboard
