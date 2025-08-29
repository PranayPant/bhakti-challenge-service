import time
from datetime import timedelta


async def profile_async(func, *args, **kwargs):
    start_time = time.time()
    result = await func(*args, **kwargs) if hasattr(func, '__await__') else func(*args, **kwargs)
    elapsed = time.time() - start_time
    td = timedelta(seconds=elapsed)
    total_seconds = int(td.total_seconds())
    _, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_taken = f"{minutes:02}m{seconds:02}s"
    return result, elapsed, time_taken
