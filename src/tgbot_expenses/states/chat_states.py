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
    DataConfirmation = State()


class StateSettings(StatesGroup):
    """
    StateSettings state
    """
    MainMenu = State()
    ChangeLimit = State()
    NewLimit = State()
    ChangeBill = State()
    AddBill = State()
    AmountBill = State()
    DeleteBill = State()
    ChangeCategory = State()
    AddCategory = State()
    CategoryLimit = State()
    DeleteCategory = State()


class StateCurrencyExchange(StatesGroup):
    """
    StateCurrencyExchange state
    """
    FromBill = State()
    FromBillAmount = State()
    ToBill = State()
    ToBillAmount = State()
    DataConfirmation = State()


class StateInvalid(StatesGroup):
    """
    StateInvalid state
    """
    InvalidAmount = State()
