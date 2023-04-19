import asyncio
import logging

from aiogram.utils import executor

from src.tgbot_expenses.bot.initialization_bot import bot
from src.tgbot_expenses.dialogs import *

logger = logging.getLogger(__name__)


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


if __name__ == '__main__':
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(main())
        executor.start_polling(bot, skip_updates=False, loop=loop)
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
