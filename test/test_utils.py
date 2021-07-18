from my_utils import utils


def test_batch():
    l = [1, 2, 3, 4, 5, 6, 7]
    expected_2 = [[1, 2], [3, 4], [5, 6], [7]]
    expected_3 = [[1, 2, 3], [4, 5, 6], [7]]
    for i, l_batch in enumerate(utils.batch(l, n=2)):
        assert l_batch == expected_2[i]
    for i, l_batch in enumerate(utils.batch(l, n=3)):
        assert l_batch == expected_3[i]
