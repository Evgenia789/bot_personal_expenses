from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_main_menu() -> InlineKeyboardMarkup:
    """
    Generating a keyboard with main menu buttons.
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
