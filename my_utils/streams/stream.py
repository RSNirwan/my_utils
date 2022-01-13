from typing import Any, Callable, Coroutine

from .components import Comparable, SortedList, DictSortedByKeys
from .components import producer, transformation, trash_transformation, sink


class Stream:
    def __init__(
        self,
        elements: SortedList[Comparable],
        initial_state: Any,
        update_state: Callable[[Any, Any, Comparable, Comparable], Any],
        collector: Callable[[Any], None],
    ):
        self.elements = elements
        self._initial_state = initial_state
        self._update_state = update_state
        self._sink = self._init_sink(collector)
        self._transformations = self._init_transformations()
        self._trash_transformation = self._init_trash_transformation(sink=None)
        self._producer = self._init_producer()

    def __call__(self, inp: Any) -> None:
        self._producer(inp)

    def _init_sink(self, collector: Callable) -> Coroutine:
        s = sink(collector)
        s.__next__()
        return s

    def _init_transformation(
        self, start: Comparable, end: Comparable, next_transformation: Coroutine
    ) -> Coroutine:
        trafo = transformation(
            start=start,
            end=end,
            next_transformation=next_transformation,
            sink=self._sink,
            initial_state=self._initial_state,
            update_state=self._update_state,
        )
        trafo.__next__()
        return trafo

    def _init_transformations(self) -> DictSortedByKeys[Comparable, Coroutine]:
        trafos = {}
        for start, end in zip(self.elements[::-1][1:], self.elements[1:][::-1]):
            next_trafo = None if len(trafos) == 0 else trafos[end]
            trafos[start] = self._init_transformation(start, end, next_trafo)
        return dict(reversed(trafos.items()))

    def _init_trash_transformation(self, sink) -> Coroutine:
        initial_state = 0
        update_state = lambda state, inp, start, end: state + 1

        trash_trafo = trash_transformation(
            self.elements[0], self.elements[-1], sink, initial_state, update_state
        )
        trash_trafo.__next__()
        return trash_trafo

    def _init_producer(self) -> Callable[[Any], None]:
        return lambda inp: producer(
            inp, self._trash_transformation, self._transformations, self.elements
        )
