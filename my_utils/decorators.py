import warnings
from inspect import getsource
from functools import wraps
from pathlib import Path
import json
import logging
from types import FunctionType
from typing import Callable, Any, Dict, List, Union, Tuple
from hashlib import md5


from my_utils import settings


def _read_json(fp: Path) -> Any:
    with fp.open() as f:
        ret = json.loads(f.read())
    return ret


def _save_json(obj: Any, fp: Path) -> None:
    with fp.open("w") as f:
        json.dump(obj, f)


def cache_decorator_factory(cache_dir: Path, hash_f: Callable) -> Callable:
    """
    Creates a cache decorator.

    Parameters
    ----------
    cache_dir : Path
        Path, where function output are save and read from.
    hash_f : Callable
        function excepting 3 parameters (func, args, kwargs) and returning
        a string that is used to validated if function was called with given
        args and kwargs already.

    Returns
    -------
    cached : Callable
        decorator used to memoizing returned values of decorated function.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)

    def cached(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            inp_hash = hash_f(func, args, kwargs)
            file_name = cache_dir / f"cache_{inp_hash}.json"
            if file_name.exists():
                logging.info(f"returning cached values with hash {inp_hash}.")
                ret_val = _read_json(file_name)
            else:
                ret_val = func(*args, **kwargs)
                _save_json(ret_val, file_name)
            return ret_val

        return wrapper

    return cached


def shallow_cache(f: Callable) -> Callable:
    """
    shallow cache decorator that caches based on function name, body
    and its arguments only.
    First, hash of function name, args and kwargs is calculated and
    then return value of the functions is saved with json.dump.
    NOTE: Callables in args and kwargs are ignored giving a warning.
    """
    myhashf = lambda x: md5(x.encode("ascii")).hexdigest()

    def make_dumpable(arg: Union[Tuple, Dict], fname) -> Union[Tuple, Dict]:
        def f(inp):
            if isinstance(inp, FunctionType):
                warnings.warn(
                    f"Ignoring callable while caching {fname}.",
                    UserWarning,
                )
                return None
            return inp

        if type(arg) == tuple:
            return tuple(map(f, arg))
        if type(arg) == dict:
            return {k: f(v) for k, v in arg.items()}

    def hash_f(func: Callable, args: Any, kwargs: Any) -> str:
        h = myhashf(
            json.dumps(
                (
                    func.__name__,
                    getsource(func),
                    make_dumpable(args, func.__name__),
                    make_dumpable(kwargs, func.__name__),
                )
            )
        )
        logging.debug(f"hash of {(func.__name__, args, kwargs)}: {h}.")
        return h

    cache_dir = settings.cache_dir()
    return cache_decorator_factory(cache_dir, hash_f)(f)
