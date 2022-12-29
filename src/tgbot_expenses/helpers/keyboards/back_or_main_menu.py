from aiogram import types


def get_keyboard_back_or_main_menu(back_button: bool=True,
                                   main_menu_button: bool=True
                                   ) -> types.InlineKeyboardMarkup:
    """
    Generating a keyboard with back or main_menu buttons.
    """
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    if back_button:
        keyboard.add(
            types.InlineKeyboardButton(
                text="Back",
                callback_data="back")
        )
    if main_menu_button:
        keyboard.add(
            types.InlineKeyboardButton(
                text="Go back to the main menu",
                callback_data="start_over")
        )

    return keyboard
