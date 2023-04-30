import asyncio
import logging
from typing import Any, Callable


def retry(max_retries: int, retry_delay: int) -> Callable:
    """
    Decorator function that adds retry functionality to a function.

    :max_retries: The maximum number of times to retry the function.
    :retry_delay: The initial delay (in seconds) between retries.

    :return: The wrapper function that adds retry functionality to
             the original function.
    :raise: If the maximum number of retries is exceeded,
            an error will be raised.
    """
    def decorator(func: Callable) -> Callable:
        async def retry_wrapper_function(*args, **kwargs) -> Any:
            for i in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    logging.error(f"Error getting accounts: {e}")
                    if i < max_retries - 1:
                        logging.info(f"Retrying in {retry_delay} seconds...")
                        await asyncio.sleep(retry_delay)
                    else:
                        raise
        return retry_wrapper_function
    return decorator
