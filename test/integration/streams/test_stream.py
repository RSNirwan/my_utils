from typing import Any
from dataclasses import dataclass

import pytest

from my_utils.streams.stream import Stream


@dataclass
class Inp:
    start: int  # required
    end: int  # required
    value: Any  # optional


@pytest.fixture
def inps():
    return [
        Inp(start=5, end=11, value="sth"),
        Inp(start=11, end=12, value="sth"),
        Inp(start=14, end=22, value="sth"),
        Inp(start=0, end=9, value="sth"),
    ]


def test_Stream(inps):
    elements = [10, 15, 20]  # will create 2 trafos (10, 15) and (15, 20)
    initial_state = 0

    def update_state(state, inp, start, end):
        diff = min(inp.end, end) - max(inp.start, start)
        return state + diff

    a = []
    collector = lambda x: a.append(x)

    stream = Stream(elements, initial_state, update_state, collector)
    for inp in inps:
        stream(inp)
    stream(None)  # will close all transformations, which then send their data to sink
    assert a == [3, 5]  # state of each trafo
