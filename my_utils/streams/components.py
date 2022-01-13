from copy import deepcopy
import logging
from typing import Any, Callable, Coroutine, List, Union, Dict


log = logging.getLogger(__name__)

Comparable = Any
SortedList = List
DictSortedByKeys = Dict


def producer(
    inp: Any,
    trash_transformation: Coroutine,
    transformations: DictSortedByKeys[Comparable, Coroutine],
    elements: List[Comparable],
) -> None:
    if inp is None:
        trash_transformation.close()
        list(transformations.values())[0].close()
    else:
        start = start_key(inp, elements)
        if start is not None:
            transformations[start].send(inp)
        else:
            trash_transformation.send(inp)


def trash_transformation(
    start: Comparable,
    end: Comparable,
    sink: Coroutine,
    initial_state: Any,
    update_state: Callable[[Any, Any, Comparable, Comparable], Any],
) -> None:
    state = deepcopy(initial_state)
    try:
        while True:
            inp = yield
            state = update_state(state, inp, start, end)
    except GeneratorExit:
        if sink is not None:
            sink.send(state)
        else:
            log.info(f"trash_transformation state at closing: {state}")


def transformation(
    start: Comparable,
    end: Comparable,
    next_transformation: Union[Coroutine, None],
    sink: Coroutine,
    initial_state: Any,
    update_state: Callable[[Any, Any, Comparable, Comparable], Any],
) -> None:
    state = deepcopy(initial_state)
    try:
        while True:
            inp = yield
            state = update_state(state, inp, start, end)
            if (inp.end > end) and (next_transformation is not None):
                next_transformation.send(inp)
    except GeneratorExit:
        sink.send(state)
        if next_transformation is not None:
            next_transformation.close()
        else:
            sink.close()


def sink(collector: Callable) -> None:
    try:
        while True:
            inp = yield
            collector(inp)
    except GeneratorExit:
        pass


def start_key(inp: Any, elements: SortedList[Comparable]) -> Comparable:
    if (inp.end < elements[0]) or (inp.start > elements[-1]):
        return None
    if inp.start < elements[0]:
        return elements[0]
    for i, next_elem in enumerate(elements[1:]):
        if inp.start < next_elem:
            return elements[i]
