from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_back_or_main_menu(back_button: bool = True,
                                   main_menu_button: bool = True
                                   ) -> InlineKeyboardMarkup:
    """
    Returns an InlineKeyboardMarkup object representing a keyboard
    with back and/or main menu buttons.

    Examples:

        To generate a keyboard with both back and main menu buttons:

        .. code-block:: python3

            keyboard = get_keyboard_back_or_main_menu()

        To generate a keyboard with only the main menu button:

        .. code-block:: python3

            keyboard = get_keyboard_back_or_main_menu(back_button=False)

        To generate a keyboard with only the back button:

        .. code-block:: python3

            keyboard = get_keyboard_back_or_main_menu(main_menu_button=False)

    :param back_button: Whether to include a "Back" button in the keyboard
                        (default True).
    :type back_button: bool
    :param main_menu_button: Whether to include a "Go back to the main menu"
                             button in the keyboard (default True).
    :type main_menu_button: bool

    :return: InlineKeyboardMarkup
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    if back_button:
        keyboard.add(InlineKeyboardButton(text="Back",
                                          callback_data="back"))
    if main_menu_button:
        keyboard.add(InlineKeyboardButton(text="Go back to the main menu",
                                          callback_data="start_over"))

    return keyboard
