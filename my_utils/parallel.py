import multiprocessing as mp
from typing import Any, Callable, Iterable, Iterator
from multiprocessing import Pool as _Pool

from pathos.multiprocessing import ProcessingPool as Pool


def pmap(func: Callable, input: Iterable, processes: int = 0) -> Iterator:
    """
    Parallel map.
    @todo: extend to process and yield batches.
    """
    n_p = mp.cpu_count() if processes <= 0 else processes
    with Pool(n_p) as p:
        out = p.map(func, input)
    for o in out:
        yield o


def _pmap(func: Callable, input: Iterable, processes: int = 0) -> Iterable:
    n_p = mp.cpu_count() if processes <= 0 else processes
    with _Pool(n_p) as p:
        out = p.map(func, input)
    for o in out:
        yield o


def pmaf(funcs: Iterable[Callable], param: Any, processes: int = 0) -> Iterator:
    """
    Parallel maf.
    like map, but input is list of functions which are applied to one parameter.
    """
    return pmap(lambda f: f(param), funcs, processes=processes)
