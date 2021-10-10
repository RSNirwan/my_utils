import numpy as np
import pytest

from my_utils import scale


def test_MAPE():
    @scale.expectation(axis0=scale.Constant(), axis1=scale.Exponential(0.4))
    def mape_mat(real: "matrix", pred: "matrix") -> "matrix":
        return np.fabs(real, pred) / np.fabs(real)

    real = np.random.normal(size=(10, 12))
    pred = real + 0.01 * np.random.normal(size=(10, 12))
    expectation = mape_mat(real, pred)

    assert isinstance(expectation, float)
    assert expectation > 0


# test for different N with parameterize
def test_Exponential():
    weights = scale.Exponential(0.2)(5)
    assert np.allclose(np.sum(weights), 1.0)
    assert np.all(np.array(weights) >= 0.0)


def test_Linear():
    weights = scale.Linear()(5)
    assert np.allclose(np.sum(weights), 1.0)
    assert np.all(np.array(weights) >= 0.0)


def test_Constant():
    weights = scale.Constant()(5)
    assert np.allclose(np.sum(weights), 1.0)
    assert np.all(np.array(weights) >= 0.0)


def test_Custom():
    _weights = [0.2, 0.3, 0.5]
    weights = scale.Custom(_weights)(len(_weights))
    assert np.allclose(np.sum(weights), 1.0)
    assert np.all(np.array(weights) >= 0.0)
    assert weights == _weights


def test_scale_axis_0():
    @scale.scale_axis(scale.Exponential(0.5), axis=0)
    def matrix():
        return np.ones(shape=(5, 6))

    assert np.allclose(np.sum(matrix(), axis=0), np.ones(shape=6))


def test_scale_axis_1():
    @scale.scale_axis(scale.Linear(), axis=1)
    def matrix():
        return np.ones(shape=(5, 6))

    assert np.allclose(np.sum(matrix(), axis=1), np.ones(shape=5))


def test_scale():
    @scale.scale(axis0=scale.Exponential(0.2), axis1=scale.Constant())
    def matrix():
        return np.ones(shape=(5, 6))

    assert np.allclose(np.sum(matrix()), 1.0)


def test_expectation():
    @scale.expectation(axis0=scale.Exponential(0.2), axis1=scale.Constant())
    def matrix():
        return np.ones(shape=(5, 6))

    assert np.allclose(matrix(), 1.0)
