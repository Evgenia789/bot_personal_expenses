import asyncio
import logging
import os

from aiogram.contrib.middlewares.logging import LoggingMiddleware
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
Bot.dispatch.middleware.setup(LoggingMiddleware())


async def main():
    """
    Initializes the logging configuration, loads the "dialogs" module,
    and starts the bot by polling for updates.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename='main.log',
        filemode='w'
    )
    logger.error("Starting bot")

    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, load_module, "dialogs",
                               os.path.abspath("src"))

    executor.start_polling(bot, skip_updates=False)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
