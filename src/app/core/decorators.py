import random
from datetime import datetime
from time import sleep


def log_execution_time(func):
    def decorator(*args, **kwargs):
        start_time = datetime.now()
        sleep(random.uniform(0.1,1)) # to simulate a processing behavior
        result = func(*args, **kwargs)
        end_time = datetime.now()

        print(f"Execution time: {str(end_time - start_time)}")

        return result

    return decorator

def print_method_signature(func):
    def decorator(*args, **kwargs):

        args_str = ", ".join(map(str, args))

        # (expression for item in iterable) is a generator expression to generate an iterable
        # join expects iterable of strings to loop provided strings
        kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())

        signature = ", ".join(filter(None, [args_str, kwargs_str]))

        print(f"Method signature: {func.__name__}({signature})")

        result = func(*args, **kwargs)
        return result
    return decorator
