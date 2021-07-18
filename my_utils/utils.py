from typing import Callable, Iterable, Iterator, Any


def batch(iterable: Iterable, n: int = 1) -> Iterator:
    """
    Example
    -------
    >>> a = [1,2,3,4,5,6,7,8]
    >>> list(batch(a, n=3))
    [[1, 2, 3], [4, 5, 6], [7, 8]]
    """
    l = len(iterable)
    for idx in range(0, l, n):
        yield iterable[idx : min(idx + n, l)]
