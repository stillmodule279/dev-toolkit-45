import time
import functools
import random

def retry_operation(max_attempts=3, delay=1.0, backoff=2.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    time.sleep(current_delay)
                    current_delay *= backoff + (random.random() * 0.1)
        return wrapper
    return decorator

class NetworkHandler:
    @retry_operation(max_attempts=4, delay=0.5)
    def fetch_data(self, url):
        # Simulate unstable network response
        if random.random() < 0.7:
            raise ConnectionError("Unstable connection triggered")
        return {"status": 200, "payload": "data"}

if __name__ == '__main__':
    client = NetworkHandler()
    try:
        result = client.fetch_data('https://api.dev.local')
        print(f"Success: {result}")
    except Exception as err:
        print(f"Final failure: {err}")