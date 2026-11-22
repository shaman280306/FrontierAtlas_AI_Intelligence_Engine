import asyncio
import functools
import random
import time
from typing import Callable, Any, Tuple, Type
import logging

logger = logging.getLogger(__name__)

def async_retry(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    jitter: bool = True,
    retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,)
) -> Callable:
    """
    Asynchronous exponential backoff decorator with full jitter.
    Handles rate-limiting (429), server errors (5xx), and network timeouts.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            retries = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except retryable_exceptions as e:
                    retries += 1
                    if retries > max_retries:
                        logger.error(f"Function {func.__name__} failed permanently after {max_retries} retries: {e}")
                        raise e
                    
                    # Compute exponential backoff with jitter
                    backoff = min(max_delay, base_delay * (2 ** (retries - 1)))
                    delay = random.uniform(0.5 * backoff, backoff) if jitter else backoff
                    logger.warning(
                        f"Retry {retries}/{max_retries} for {func.__name__} due to {type(e).__name__}: {e}. "
                        f"Backing off for {delay:.2f}s."
                    )
                    await asyncio.sleep(delay)
        return wrapper
    return decorator
