from __future__ import annotations

from array import array as _array, typecodes
from typing import Generic, Iterable, TypeVar

__version__ = '1.0.0'
__all__ = ('SByteArray', 'ByteArray',
           'CharArray', 'UCharArray',  # aliases for byte arrays
           'UnicodeArray',
           'ShortArray', 'UShortArray',
           'IntArray', 'UIntArray',
           'LongArray', 'ULongArray',
           'LongLongArray', 'ULongLongArray',
           'FloatArray', 'DoubleArray',
           'typecodes')


T = TypeVar('T')


class ArrayType(Generic[T]):
    def __init__(self, typecode: str, _type: type[T]) -> None:
        self.typecode = typecode
        self.type = _type

    def __call__(self, initializer: bytes | Iterable[T] = (), /) -> _array[T]:
        return _array(self.typecode, initializer)


SByteArray = ArrayType('b', int)
"""Stores signed chars (signed bytes). [-128; 127]"""
ByteArray = ArrayType('B', int)
"""Stores unsigned chars (unsigned bytes). [0; 255]"""
UnicodeArray = ArrayType('u', str)
"""Stores Unicode strings."""
ShortArray = ArrayType('h', int)
"""Stores signed 16-bit integers. [-32768; 32767]"""
UShortArray = ArrayType('H', int)
"""Stores unsigned 16-bit integers. [0; 65535]"""
IntArray = ArrayType('i', int)
"""
Stores *at least* signed 16-bit integers. [-32768; 32767]

Note:
    Python documentation states that ``array('i')`` elements *minimal* size is **2 bytes**.

    However, in most cases you deal with **32-bit** integers. [-2147483648; 2147483647]
"""
UIntArray = ArrayType('I', int)
"""
    Stores at least unsigned 16-bit integers. [0; 65535]

Note:
    Python documentation states that ``array('I')`` elements *minimal* size is **2 bytes**.

    However, in most cases you deal with **32-bit** integers. [0; 4294967295]
"""
LongArray = ArrayType('l', int)
"""Stores signed 32-bit integers. [-2147483648; 2147483647]"""
ULongArray = ArrayType('L', int)
"""Stores unsigned 32-bit integers. [0; 4294967295]"""
LongLongArray = ArrayType('q', int)
"""Stores signed 64-bit integers. [−9223372036854775807; 9223372036854775807]"""
ULongLongArray = ArrayType('Q', int)
"""Stores signed 64-bit integers. [0; 18446744073709551615]"""
FloatArray = ArrayType('f', float)
"""Stores single-precision floating-point numbers."""
DoubleArray = ArrayType('d', float)
"""Stores double-precision floating-point numbers."""

CharArray = SByteArray
UCharArray = ByteArray


def demo():
    print(f'{ShortArray([-4, -3, -2, -1, 0, 1, 2, 3, 4]) = }')
    print(f'{UIntArray([100_000, 100_001, 100_002, 100_003, 100_004]) = }')
    print(f'{ULongArray().itemsize = }')


if __name__ == '__main__':
    demo()
