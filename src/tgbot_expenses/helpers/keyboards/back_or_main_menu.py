from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_back_or_main_menu(back_button: bool = True,
                                   main_menu_button: bool = True
                                   ) -> InlineKeyboardMarkup:
    """
    Returns an InlineKeyboardMarkup object representing a keyboard
    with back and/or main menu buttons.

    Args:
        back_button (bool): Whether to include a "Back" button in
                            the keyboard (default True).
        main_menu_button (bool): Whether to include a "Go back to
                                 the main menu" button in the keyboard
                                 (default True).

    Returns:
        InlineKeyboardMarkup: An InlineKeyboardMarkup object representing
                              the generated keyboard.

    Examples:
        To generate a keyboard with both back and main menu buttons, use:
        >>> keyboard = get_keyboard_back_or_main_menu()

        To generate a keyboard with only the main menu button, use:
        >>> keyboard = get_keyboard_back_or_main_menu(back_button=False)

        To generate a keyboard with only the back button, use:
        >>> keyboard = get_keyboard_back_or_main_menu(main_menu_button=False)
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    if back_button:
        keyboard.add(InlineKeyboardButton(text="Back",
                                          callback_data="back"))
    if main_menu_button:
        keyboard.add(InlineKeyboardButton(text="Go back to the main menu",
                                          callback_data="start_over"))

    return keyboard
