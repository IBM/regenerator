import string

from regenerator import Stream

from .util import *

def test_from_iterable():
    iter_stream = Stream.from_iterable([1, 2, 3])
    validate_stream(iter_stream, 3, int)

def test_from_iterable_tuple():
    values = [
        [1, 2, 3],
        ['a', 'b', 'c'],
        ['x', 'y', 'z'],
    ]

    iter_stream = Stream.from_iterable(values)
    validate_stream(iter_stream, 3, list, 3)

def test_custom_type(custom_stream, custom_stream_class):
    custom_stream2 = custom_stream_class.from_iterable(string.ascii_lowercase)
    validate_stream(custom_stream2, 26, str, 1)

    assert isinstance(custom_stream2, custom_stream_class)
