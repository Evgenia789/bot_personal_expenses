"""
This module defines the load_config function to read and load a configuration
file in ini format into a Config object.
The Config object is defined as a dataclass containing TgBot, and
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
class PostgresDBConfig:
    """
    Represents a PostgreSQL database configuration.

    Attributes:
        postgres_host (str): The hostname of the PostgreSQL server.
        postgres_port (int): The port number of the PostgreSQL server.
        postgres_user (str): The username for accessing the database.
        postgres_password (str): The password for accessing the database.
        postgres_db (str): The name of the PostgreSQL database to use.
        _db_url (str): The URL for connecting to the PostgreSQL database.
    """
    postgres_host: str
    postgres_port: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    _db_url: str = None

    @property
    def db_url(self) -> str:
        if self._db_url is None:
            self._db_url = (f"postgresql+asyncpg://{self.postgres_user}:"
                            f"{self.postgres_password}@{self.postgres_host}:"
                            f"{self.postgres_port}/{self.postgres_db}")
        return self._db_url


@dataclass
class Config:
    """
    Configuration object that contains all the configuration data.

    Attributes:
        tg_bot (TgBot): Telegram Bot token configuration.
        postgres_db (PostgresDB): PostgreSQL database configuration.
    """
    tg_bot: TgBot
    postgres_db: PostgresDBConfig

    @classmethod
    def load_config(cls, path: str) -> 'Config':
        """
        Load the configuration file in ini format located at the given path.

        :param path: The path to the configuration file.
        :type path: str

        :return: A `Config` object containing all the configuration data.

        :raises MissingSectionHeaderError: If the configuration file is missing
                                           a section header.
        :raises ParsingError: If there is an error parsing
                              the configuration file.
        """
        config = configparser.ConfigParser()
        config.read(path, encoding="utf-8")

        tg_bot = config["tg_bot"]
        postgres_db = config["postgres_database"]

        return cls(
            tg_bot=TgBot(token=tg_bot.get("TELEGRAM_TOKEN")),
            postgres_db=PostgresDBConfig(**postgres_db)
        )
