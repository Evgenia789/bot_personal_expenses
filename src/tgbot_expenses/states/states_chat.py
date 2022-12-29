from aiogram.dispatcher.filters.state import State, StatesGroup


class StateChat(StatesGroup):
    """
    StateChat state
    """
    MainMenu = State()
    ShowStatistic = State()
    Category = State()
    Bill = State()
    Amount = State()
    InvalidAmount = State()
    DataConfirmation = State()
