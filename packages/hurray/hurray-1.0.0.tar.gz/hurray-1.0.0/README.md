# hurray

[![PyPI release]][pypi] 
[![Python supported versions]][pypi]
[![License]](./LICENSE)

hurray is a simple package containing a collection of wrappers around Python's builtin 'array' module.

```python
from hurray import ShortArray, UIntArray, ULongArray

arr1 = ShortArray([-4, -3, -2, -1, 0, 1, 2, 3, 4])
arr2 = UIntArray([100_000, 100_001, 100_002, 100_003, 100_004])
empty = ULongArray()

print(arr1)  # array('h', [-4, -3, -2, -1, 0, 1, 2, 3, 4])
print(arr2)  # array('I', [100000, 100001, 100002, 100003, 100004])
print(empty.itemsize)  # 4
```

*Special thanks to [trag1c], [CircuitSacul], [Micael Jarniac], [bswck] for helping to make this silly package.*

[pypi]: https://pypi.org/project/hurray/
[PyPI Release]: https://img.shields.io/pypi/v/hurray.svg?label=pypi&color=green
[Python supported versions]: https://img.shields.io/pypi/pyversions/hurray.svg?label=%20&logo=python&logoColor=white
[License]: https://img.shields.io/pypi/l/hurray.svg?style=flat&label=license

[trag1c]: https://github.com/trag1c
[CircuitSacul]: https://github.com/CircuitSacul
[Micael Jarniac]: https://github.com/MicaelJarniac
[bswck]: https://github.com/bswck