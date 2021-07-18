from typing import Callable, Iterable, Iterator, Any


def batch(iterable: Iterable, n: int = 1) -> Iterator:
    """
    Example
    -------
    >>> a = [1,2,3,4,5,6,7,8]
    >>> list(batch(a, n=3))
    [[1, 2, 3], [4, 5, 6], [7, 8]]
    """
    it = iter(iterable)
    flag = True
    while flag:
        ret = []
        for _ in range(n):
            try:
                ret.append(next(it))
            except StopIteration:
                flag = False
                break
        yield ret


def maf(funcs: Iterable[Callable], param: Any) -> Iterator:
    """
    map for functions.
    Like map, but input is list of functions which are applied to one parameter.

    Example
    -------
    >>> fs = [lambda x: x + 1, lambda x: x + 2]
    >>> list(maf(fs, 1))
    [2, 3]
    """
    return map(lambda f: f(param), funcs)
