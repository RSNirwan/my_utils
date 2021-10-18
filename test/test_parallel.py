from my_utils import parallel


def f_map(a):
    return a + 1


def test_pmap():
    input = 10 * [1]
    expected_out = 10 * [2]
    assert list(parallel.pmap(f_map, input)) == expected_out


def test_pmaf():
    f = [lambda x: x + 1, lambda x: x + 2, lambda x: x + 3]
    a = 2
    assert list(parallel.pmaf(f, a)) == [3, 4, 5]


def test__pmap():
    input = 10 * [1]
    expected_out = 10 * [2]
    assert list(parallel._pmap(f_map, input)) == expected_out
