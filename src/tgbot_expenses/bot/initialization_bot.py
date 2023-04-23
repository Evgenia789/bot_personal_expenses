from aiogram.contrib.middlewares.logging import LoggingMiddleware

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.config import Config
from src.tgbot_expenses.middlewares import (AuthorizationMiddleware,
                                            StartOrContinueMiddleware,
                                            UnrecognizedMessageMiddleware)

config = Config.load_config("bot.ini")

bot = Bot(config.tg_bot.token)
Bot.dispatch.middleware.setup(StartOrContinueMiddleware())
Bot.dispatch.middleware.setup(UnrecognizedMessageMiddleware())
Bot.dispatch.middleware.setup(AuthorizationMiddleware())
Bot.dispatch.middleware.setup(LoggingMiddleware())
