from time import time


def timer(f):
    """decorator to measure run time of a function f"""

    def wrapper(*args, **kwargs):
        start = time()
        rv = f(*args, **kwargs)
        dtime = time() - start
        print(f"timer({f.__name__}): {dtime}[sec]")
        return rv

    return wrapper
