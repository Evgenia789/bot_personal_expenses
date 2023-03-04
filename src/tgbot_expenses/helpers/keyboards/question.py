from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_question(button_names: str,
                          button_back: bool = False) -> InlineKeyboardMarkup:
    """
    Returns an InlineKeyboardMarkup object representing a keyboard for asking
    a question with customizable buttons.

    The generated keyboard has buttons corresponding to the strings in
    the 'button_names' argument. Each button triggers a callback with the
    string as its payload. If 'button_back' is True, an additional "Back"
    button is added to the keyboard which triggers a "back" callback.

    Examples:

        To generate a keyboard for asking a question with three buttons
        ("Option 1", "Option 2", and "Option 3"):

        .. code-block:: python3

            keyboard = get_keyboard_question("Option 1;Option 2;Option 3")

        To generate the same keyboard with a "Back" button:

        .. code-block:: python3

            keyboard = get_keyboard_question(
                "Option 1;Option 2;Option 3", button_back=True
            )

    :param button_names: A semicolon-delimited string of button names to
                         display on the keyboard.
    :type button_names: str
    :param button_back: Whether to include a "Back" button on the keyboard.
                        Defaults to False.
    :type button_back: bool, optional

    :return: InlineKeyboardMarkup
    """
    buttons: List[InlineKeyboardButton] = []
    button_names = button_names.split(";")
    for button_name in button_names:
        buttons.append(InlineKeyboardButton(text=button_name,
                                            callback_data=button_name))

    if button_back:
        buttons.append(InlineKeyboardButton(text="Back",
                                            callback_data="back"))

    return InlineKeyboardMarkup(row_width=2).add(*buttons)
