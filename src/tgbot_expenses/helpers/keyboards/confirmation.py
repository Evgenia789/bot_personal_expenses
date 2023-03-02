from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_confirmation() -> InlineKeyboardMarkup:
    """
    Returns an InlineKeyboardMarkup object representing a keyboard
    for confirming or cancelling an action.

    Returns:
        InlineKeyboardMarkup: An InlineKeyboardMarkup object representing
                              the generated keyboard.

    Examples:
        To generate a keyboard for confirming or cancelling an action, use:
        >>> keyboard = get_keyboard_confirmation()
    """
    keyboard = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(text="Confirm",
                             callback_data="confirm"),
        InlineKeyboardButton(text="Cancel",
                             callback_data="cancel")
    )

    return keyboard
