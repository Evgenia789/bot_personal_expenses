"""
This module defines the load_config function to read and load a configuration
file in ini format into a Config object.
The Config object is defined as a dataclass containing TgBot, AllowedIds, and
GoogleTables objects, also defined as dataclasses.

This module requires the configparser and dataclasses modules to be imported.

Example usage:
    config = load_config('config.ini')
"""
import configparser
from dataclasses import dataclass


@dataclass
class TgBot:
    """
    Telegram Bot token configuration.

    Attributes:
        token (str): Telegram Bot token.
    """
    token: str


@dataclass
class AllowedIds:
    """
    Allowed user IDs configuration.

    Attributes:
        id_1 (int): First allowed user ID.
        id_2 (int): Second allowed user ID.
    """
    id_1: int
    id_2: int


@dataclass
class GoogleTables:
    """
    Google Sheets tables configuration.

    Attributes:
        spreadsheet (str): Name of the spreadsheet.
        expenses (str): Name of the expenses table.
        incomes (str): Name of the incomes table.
        currency (str): Name of the currency table.
        total_amount (str): Name of the total amount table.
    """
    spreadsheet: str
    expenses: str
    incomes: str
    currency: str
    total_amount: str


@dataclass
class Config:
    """
    Configuration object that contains all the configuration data.

    Attributes:
        tg_bot (TgBot): Telegram Bot token configuration.
        ids (AllowedIds): Allowed user IDs configuration.
        googletables (GoogleTables): Google Sheets tables configuration.
    """
    tg_bot: TgBot
    ids: AllowedIds
    googletables: GoogleTables


def load_config(path: str) -> Config:
    """
    Load the configuration file in ini format located at the given path.

    :param path: The path to the configuration file.
    :type path: str

    :return: A `Config` object containing all the configuration data.

    :raises MissingSectionHeaderError: If the configuration file is missing
                                       a section header.
    :raises ParsingError: If there is an error parsing the configuration file.
    """
    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")

    tg_bot = config["tg_bot"]
    ids = config["allowed_ids"]
    googletables = config["google_tables"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot.get("TELEGRAM_TOKEN")
        ),
        ids=AllowedIds(
            id_1=ids.getint("ID_1"),
            id_2=ids.getint("ID_2")
        ),
        googletables=GoogleTables(
            spreadsheet=googletables.get("spreadsheet"),
            expenses=googletables.get("expenses"),
            incomes=googletables.get("incomes"),
            currency=googletables.get("currency"),
            total_amount=googletables.get("total_amount")
        )
    )
