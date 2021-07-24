from pathlib import Path
from unittest import mock
from typing import Callable
import json

import pytest

from my_utils import decorators


def test_cache_decorator_factory(tmpdir):
    m = mock.Mock()
    hash_f = lambda f, args, _: hash(f"{f.__name__}-{json.dumps(args)}")

    @decorators.cache_decorator_factory(Path(tmpdir) / "cache", hash_f)
    def add_one(a: int) -> int:
        m()
        return a + 1

    assert add_one(1) == 2  # return value is cached
    assert add_one(1) == 2  # return value is read, no function call
    assert m.call_count == 1  # second call didn't increase the counter
    assert add_one(2) == 3
    assert m.call_count == 2


@mock.patch("my_utils.decorators.settings.cache_dir")
def test_shallow_cache(cache_dir, tmpdir):
    m = mock.Mock()
    cache_dir.return_value = Path(tmpdir) / "cache"

    @decorators.shallow_cache
    def sub_one(a: int) -> int:
        m()
        return a - 1

    assert sub_one(2) == 1  # return value is cached
    assert sub_one(2) == 1  # return value is read, no function call
    assert m.call_count == 1  # second call didn't increase the counter
    assert sub_one(5) == 4
    assert m.call_count == 2


@mock.patch("my_utils.decorators.settings.cache_dir")
def test_shallow_cache_functiontype(cache_dir, tmpdir):
    m = mock.Mock()
    cache_dir.return_value = Path(tmpdir) / "cache"

    @decorators.shallow_cache
    def call_f(f: Callable, a: int) -> int:
        m()
        return f(a)

    with pytest.warns(UserWarning, match="Ignoring callable"):
        assert call_f(lambda x: x + 10, 1) == 11  # return value is cached
        assert call_f(lambda x: x + 10, 1) == 11  # return value is read, no call
        assert m.call_count == 1  # second call didn't increase the counter
        # ! shallow_cache ignores input callables
        assert call_f(lambda x: x + 11, 1) == 11  # return value is the one from above
        assert m.call_count == 1
        assert call_f(lambda x: x + 10, 2) == 12
        assert m.call_count == 2
