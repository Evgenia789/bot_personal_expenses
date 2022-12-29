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
class Config:
    tg_bot: TgBot
    ids: AllowedIds


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path, encoding='utf-8')

    tg_bot = config["tg_bot"]
    ids = config["allowed_ids"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot.get("TELEGRAM_TOKEN")
        ),
        ids=ids.values()
    )
