from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_question(button_names: str,
                          button_back: bool = False) -> InlineKeyboardMarkup:
    """
    Generating a keyboard with question buttons.
    """
    buttons = []
    button_names = button_names.split(";")
    for i in range(0, len(button_names)):
        buttons.append(InlineKeyboardButton(text=button_names[i],
                                            callback_data=button_names[i]))

    if button_back:
        buttons.append(InlineKeyboardButton(text="Back",
                                            callback_data="back"))

    return InlineKeyboardMarkup(row_width=2).add(*buttons)
