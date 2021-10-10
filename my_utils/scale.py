import numpy as np

_exp_weight = lambda lam, N, i: (lam - 1) / (lam ** N - 1) * lam ** i
Exponential = lambda lam: lambda N: [_exp_weight(lam, N, i) for i in range(N)]
Linear = lambda: lambda N: [2.0 / (N + 1) * (1 - i / N) for i in range(N)]
Constant = lambda: lambda N: N * [1.0 / N]
Custom = lambda weights: lambda N: weights


def scale_axis(scale_f, axis=0):
    """Example decoration: @scale_axis(Exponential(0.2), axis=1)"""

    def dec(f):
        def inner(*args, **kwargs):
            mat = np.array(f(*args, **kwargs))
            scales = np.array(scale_f(mat.shape[axis]))
            shape = [-1 if i == axis else 1 for i in range(2)]
            return np.multiply(mat, scales.reshape(shape))

        return inner

    return dec


def scale(axis0, axis1, sum=False):
    """Example decoration: @scale(Exponential(0.2), Linear())"""

    def dec(f):
        f_scaled = scale_axis(axis0, axis=0)(f)
        return scale_axis(axis1, axis=1)(f_scaled)

    sum_dec = lambda f: lambda *args, **kwargs: np.sum(dec(f)(*args, **kwargs))

    return sum_dec if sum else dec


def expectation(axis0, axis1):
    """Example decoration: @expectation(Exponential(0.2), Linear())"""
    return scale(axis0, axis1, sum=True)
