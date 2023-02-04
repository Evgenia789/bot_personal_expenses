from aiogram.dispatcher.filters.state import State, StatesGroup


class StateSettings(StatesGroup):
    """
    StateSettings state
    """
    MainMenu = State()
    ChangeLimit = State()
    NewLimit = State()
    InvalidAmount = State()
    ChangeBill = State()
    AddBill = State()
    DeleteBill = State()
    ChangeCategory = State()
    AddCategory = State()
    CategoryLimit = State()
    DeleteCategory = State()
