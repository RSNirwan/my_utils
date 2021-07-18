## utility functions (WIP)

Because I am too lazy to write these functions over and over again.

[![codecov](https://codecov.io/gh/RSNirwan/my_utils/branch/master/graph/badge.svg?token=KOTTKQ1G32)](https://codecov.io/gh/RSNirwan/my_utils)


### Install
```bash
pip install git+https://github.com/RSNirwan/my_utils
```

### Usage
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