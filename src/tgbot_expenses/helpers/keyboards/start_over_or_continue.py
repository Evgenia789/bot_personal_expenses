from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_start_over_or_continue() -> InlineKeyboardMarkup:
    """
    Returns an InlineKeyboardMarkup object representing a keyboard
    with main menu buttons.

    The generated keyboard has buttons for "Start over" and "Continue",
    allowing users to either return to the main menu or continue with
    their current task.

    Example:

        To generate a keyboard with "Start over" and "Continue" buttons:

        .. code-block:: python3

            keyboard = get_keyboard_start_over_or_continue()

    :return: InlineKeyboardMarkup
    """
    keyboard = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(text="Start over",
                             callback_data="start_over"),
        InlineKeyboardButton(text="Continue",
                             callback_data="continue")
    )

    return keyboard
