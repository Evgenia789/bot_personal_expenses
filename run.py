import asyncio
import logging
import os

from aiogram.utils import executor

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.config import load_config
from src.tgbot_expenses.middlewares import (AuthorizationMiddleware,
                                            StartOrContinueMiddleware,
                                            UnknownMiddleware)
from src.tgbot_expenses.utils.load_modules import load_module

logger = logging.getLogger(__name__)
config = load_config("bot.ini")


bot = Bot(config.tg_bot.token)
Bot.dispatch.middleware.setup(StartOrContinueMiddleware())
Bot.dispatch.middleware.setup(UnknownMiddleware())
Bot.dispatch.middleware.setup(AuthorizationMiddleware())


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger.error("Starting bot")
    load_module("dialogs", cur_dir=os.path.abspath("src"))

    executor.start_polling(bot, skip_updates=False)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
