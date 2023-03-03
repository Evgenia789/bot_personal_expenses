from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_changing_bill() -> InlineKeyboardMarkup:
    """
    Returns an InlineKeyboardMarkup object representing a keyboard
    for changing bill options.

    Example:

        To generate a keyboard for changing bill options:

        .. code-block:: python3

            keyboard = get_keyboard_changing_bill()

    :return: InlineKeyboardMarkup
    """
    keyboard = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(text="Add bill",
                             callback_data="add_bill"),
        InlineKeyboardButton(text="Delete bill",
                             callback_data="delete_bill"),
        InlineKeyboardButton(text="Back", callback_data="back")
    )

    return keyboard
