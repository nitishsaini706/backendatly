import time
from functools import wraps

def retry(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        max_retries = 3
        delay = 2
        for _ in range(max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                print(f"Error: {e}, retrying in {delay} seconds...")
                time.sleep(delay)
        raise Exception(f"Failed to complete {func.__name__} after {max_retries} attempts")
    return wrapper
