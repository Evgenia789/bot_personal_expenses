from aiogram import types


def get_keyboard_question(button_names: str, button_back: bool=False) -> types.InlineKeyboardMarkup:
    """
    Generating a keyboard with question buttons.
    """
    buttons = []
    button_names = button_names.split(";")
    for i in range(0, len(button_names)):
        buttons.append(
            types.InlineKeyboardButton(
                text=button_names[i],
                callback_data=button_names[i]
            )
        )
    
    if button_back:
        buttons.append(
            types.InlineKeyboardButton(
                text="Back",
                callback_data="back"
            )
        )

    return types. \
        InlineKeyboardMarkup(row_width=2). \
        add(*buttons)

