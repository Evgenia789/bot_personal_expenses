import configparser
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str


@dataclass
class AllowedIds:
    id_1: int
    id_2: int


@dataclass
class GoogleTableName:
    table_expenses: str
    table_incomes: str
    table_currency: str
    table_total_amount: str


@dataclass
class Config:
    tg_bot: TgBot
    ids: AllowedIds
    googletables: GoogleTableName


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path, encoding='utf-8')

    tg_bot = config["tg_bot"]
    ids = config["allowed_ids"]
    googletables = config["googletables"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot.get("TELEGRAM_TOKEN")
        ),
        ids=AllowedIds(
            id_1=ids.getint("ID_1"),
            id_2=ids.getint("ID_2")
        ),
        googletables=GoogleTableName(
            expenses=googletables.get("expenses_table"),
            incomes=googletables.get("incomes_table"),
            currency=googletables.get("currency_table"),
            total_amount=googletables.get("total_amount_table")
        )
    )
