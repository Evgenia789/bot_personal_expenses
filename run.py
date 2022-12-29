import asyncio
import logging
import os

from aiogram.utils import executor
from dotenv import load_dotenv

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.middlewares import (StartOrContinueMiddleware,
                                                     UnknownMiddleware)
from src.tgbot_expenses.utils.load_modules import loadModules

logger = logging.getLogger(__name__)


load_dotenv()
bot = Bot(os.getenv("TELEGRAM_TOKEN"))
Bot.dispatch.middleware.setup(StartOrContinueMiddleware())
Bot.dispatch.middleware.setup(UnknownMiddleware())

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    loadModules("dialogs", cur_dir=os.path.abspath("src"))
    
    executor.start_polling(bot, skip_updates=False)


if __name__ == '__main__':
    try:
        # main()
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
