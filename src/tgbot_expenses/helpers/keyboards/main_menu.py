from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_main_menu() -> InlineKeyboardMarkup:
    """
    Returns an InlineKeyboardMarkup object representing a keyboard
    to select main menu buttons.

    Example:

        To generate a keyboard to select main menu buttons:

        .. code-block:: python3

            keyboard = get_keyboard_main_menu()

    :return: InlineKeyboardMarkup
    """
    keyboard = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(text="Make expenses",
                             callback_data="make_expenses"),
        InlineKeyboardButton(text="Make incomes",
                             callback_data="make_incomes"),
        InlineKeyboardButton(text="Exchange currency",
                             callback_data="exchange_currency"),
        InlineKeyboardButton(text="Settings",
                             callback_data="settings"),
        InlineKeyboardButton(text="View statistics",
                             callback_data="view_statistics"),
        InlineKeyboardButton(text="Show currency rates",
                             callback_data="currency_rates"),
    )

    return keyboard
