from aiogram.dispatcher.filters.state import State, StatesGroup


class StateChat(StatesGroup):
    """
    Represents the state of a chat conversation.
    """
    MainMenu = State()
    ShowStatistic = State()
    Category = State()
    Bill = State()
    Amount = State()
    DataConfirmation = State()


class StateSettings(StatesGroup):
    """
    Represents the state of settings.
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
    Represents the state of a chat currency exchange rate.
    """
    FromBill = State()
    FromBillAmount = State()
    ToBill = State()
    ToBillAmount = State()
    DataConfirmation = State()


class StateInvalid(StatesGroup):
    """
    Represents the invalid state.
    """
    InvalidAmount = State()
