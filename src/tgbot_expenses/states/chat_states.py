from aiogram.dispatcher.filters.state import State, StatesGroup


class StateChat(StatesGroup):
    """
    Represents the state of a chat conversation.
    """
    MainMenu = State()
    ShowStatistic = State()
    Category = State()
    Account = State()
    Amount = State()
    DataConfirmation = State()


class StateSettings(StatesGroup):
    """
    Represents the state of settings.
    """
    MainMenu = State()
    ChangeLimit = State()
    NewLimit = State()
    ChangeAccount = State()
    AddAccount = State()
    AmountAccount = State()
    DeleteAccount = State()
    ChangeCategory = State()
    AddCategory = State()
    CategoryLimit = State()
    DeleteCategory = State()


class StateCurrencyExchange(StatesGroup):
    """
    Represents the state of a chat currency exchange rate.
    """
    FromAccount = State()
    FromAccountAmount = State()
    ToAccount = State()
    ToAccountAmount = State()
    DataConfirmation = State()


class StateInvalid(StatesGroup):
    """
    Represents the invalid state.
    """
    InvalidAmount = State()


class StateEmpty(StatesGroup):
    """
    Represents the invalid state.
    """
    InvalidEmpty = State()
