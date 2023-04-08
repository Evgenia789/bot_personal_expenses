import asyncio
import logging
import os

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.config import Config
from src.tgbot_expenses.middlewares import (AuthorizationMiddleware,
                                            StartOrContinueMiddleware,
                                            UnrecognizedMessageMiddleware)
from src.tgbot_expenses.utils.load_modules import load_module

logger = logging.getLogger(__name__)
config = Config.load_config("bot.ini")


bot = Bot(config.tg_bot.token)
Bot.dispatch.middleware.setup(StartOrContinueMiddleware())
Bot.dispatch.middleware.setup(UnrecognizedMessageMiddleware())
Bot.dispatch.middleware.setup(AuthorizationMiddleware())
Bot.dispatch.middleware.setup(LoggingMiddleware())


async def main():
    """
    Initializes the logging configuration and loads the "dialogs" module.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename='main.log',
        filemode='w'
    )
    logger.error("Starting bot")

    await load_module("dialogs", os.path.abspath("src"))


if __name__ == '__main__':
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(main())
        executor.start_polling(bot, skip_updates=False, loop=loop)
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
