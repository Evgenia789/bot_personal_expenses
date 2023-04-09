from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.tgbot_expenses.config import Config
from src.tgbot_expenses.models.expense_tracking_models import Base


class AsyncSessionWithEnter(AsyncSession):
    """
    Subclass of AsyncSession that provides support for the 'async with' syntax.

    Example usage:

    async with AsyncSessionWithEnter() as session:
        # interact with session object here

    """
    async def __aenter__(self):
        """
        Returns the session object when used in an 'async with' block.
        """
        return self

    async def __aexit__(self, exc_type, exc_val, traceback):
        """
        Rolls back any uncommitted changes when the 'async with' block
        is exited.
        """
        await super().__aexit__(exc_type, exc_val, traceback)


class AsyncPostgresDB:
    """
    An asynchronous database client for PostgreSQL.
    """
    _instance = None
    engine = None
    config = Config.load_config("bot.ini")

    def __new__(cls, *args, **kwargs):
        """
        Create a singleton instance of the AsyncPostgresDB class.

        :return: A singleton instance of the AsyncPostgresDB class.
        """
        if cls._instance is None:
            cls._instance = super(AsyncPostgresDB, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        """
        Initializes a new instance of the AsyncPostgresDB class.
        """
        if self.engine is None:
            db_config = self.config.postgres_db
            self.engine = create_async_engine(
                url=db_config.db_url,
                echo=True
            )

    async def __call__(self, *args, **kwargs) -> 'AsyncPostgresDB':
        """
        Returns the singleton instance of the AsyncPostgresDB class.
        """
        self.__init__(*args, **kwargs)
        return self.engine

    async def create_tables(self) -> None:
        """
        Creates the Category, Income, Expense, and Account tables
        if they do not exist.

        :return: None
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        return


database = AsyncPostgresDB()
