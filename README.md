## utility functions (WIP)

Because I am too lazy to write these functions over and over again.

[![codecov](https://codecov.io/gh/RSNirwan/my_utils/branch/master/graph/badge.svg?token=KOTTKQ1G32)](https://codecov.io/gh/RSNirwan/my_utils)


### Install
```bash
pip install git+https://github.com/RSNirwan/my_utils
```

### Usage

#### Basics
```python
#from my_utils import *
from my_utils import batch, pmap, maf, pmaf

a = [1,2,3,4,5,6,7]
for a_batch in batch(a, n=3): # iterate over batches
    print(a_batch)


a = range(20)
pmap(lambda x: x + 1, a)  # parallel map


fs = [lambda x: x + 1, lambda x: x + 2]
param = 2
maf(fs, param)  # equivalent to map. Inputs are multiple functions and only one parameter.
pmaf(fs, param)  # parallel maf
```

#### Timer
```python
from time import sleep
from my_utils.decorators import timer

@timer
def add5(x):
    sleep(2)
    return x + 5

_ = add5(1) # prints: timer(add5): 2.0010859966278076[sec]
```

#### Shallow cache
```python
from time import sleep
from my_utils.decorators import shallow_cache

@shallow_cache
def add5(x):
    sleep(2)
    return x + 5

_ = add5(1) # takes 2 sec to run the function
_ = add5(1) # returns cached results immediately
```

#### Scale
```python
import numpy as np
from my_utils.scale import Constant, Exponential, expectation

@expectation(axis0=Constant(), axis1=Exponential(0.4))
def mape_mat(real: "matrix", pred: "matrix") -> "matrix":
    return np.fabs(real - pred) / np.fabs(real)

real = np.random.normal(size=(10, 12))
pred = real + 0.01 * np.random.normal(size=(10, 12))
expec = mape_mat(real, pred)
```
