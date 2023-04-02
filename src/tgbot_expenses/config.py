"""
This module defines the load_config function to read and load a configuration
file in ini format into a Config object.
The Config object is defined as a dataclass containing TgBot, AllowedIds, and
PostgresDB objects, also defined as dataclasses.

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
class PostgresDB:
    """
    Represents a PostgreSQL database configuration.

    Attributes:
        db_host (str): The hostname of the PostgreSQL server.
        db_name (str): The name of the database.
        db_port (int): The port number of the PostgreSQL server.
        postgres_user (str): The username for accessing the database.
        postgres_password (str): The password for accessing the database.
        postgres_db (str): The name of the PostgreSQL database to use.
        db_url (str): The URL for connecting to the PostgreSQL database.
    """
    db_host: str
    db_port: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    db_url: str = None

    def __post_init__(self):
        if self.db_url is None:
            self.db_url = (f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.db_host}:{self.db_port}/{self.postgres_db}")


@dataclass
class Config:
    """
    Configuration object that contains all the configuration data.

    Attributes:
        tg_bot (TgBot): Telegram Bot token configuration.
        ids (AllowedIds): Allowed user IDs configuration.
        postgres_db (PostgresDB): PostgreSQL database configuration.
    """
    tg_bot: TgBot
    ids: AllowedIds
    postgres_db: PostgresDB


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
    postgres_db = config["postgres_database"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot.get("TELEGRAM_TOKEN")
        ),
        ids=AllowedIds(
            id_1=ids.getint("ID_1"),
            id_2=ids.getint("ID_2")
        ),
        postgres_db=PostgresDB(
            db_host=postgres_db.get("DB_HOST"),
            db_port=postgres_db.get("DB_PORT"),
            postgres_user=postgres_db.get("POSTGRES_USER"),
            postgres_password=postgres_db.get("POSTGRES_PASSWORD"),
            postgres_db=postgres_db.get("POSTGRES_DB"),
            db_url=PostgresDB.db_url
        )
    )
