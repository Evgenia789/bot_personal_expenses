from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_confirmation() -> InlineKeyboardMarkup:
    """
    Returns an InlineKeyboardMarkup object representing a keyboard
    for confirming or cancelling an action.

    Example:

        To generate a keyboard for confirming or cancelling an action:

        .. code-block:: python3

            keyboard = get_keyboard_confirmation()

    :return: InlineKeyboardMarkup
    """
    keyboard = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(text="Confirm",
                             callback_data="confirm"),
        InlineKeyboardButton(text="Cancel",
                             callback_data="cancel")
    )

    return keyboard
