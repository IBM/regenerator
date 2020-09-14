import string

from regenerator import Stream

from .util import *

def test_matches_init():
    generator_func = lambda: (item / 2.0 for item in range(1, 10, 2))

    init_stream = Stream(generator_func)
    validate_stream(init_stream, 5, float)

    from_stream = Stream.from_func(generator_func)
    validate_stream(init_stream, 5, float)

    for item1, item2 in zip(init_stream, from_stream):
        assert abs(item1 - item2) < 1.0e-4

def test_from_empty():
    empty_stream = Stream.from_func(lambda: iter(()))
    validate_stream(empty_stream, 0, object)

def test_custom_type(custom_stream, custom_stream_class):
    custom_stream2 = custom_stream_class.from_func(lambda: iter(string.ascii_lowercase))
    validate_stream(custom_stream2, 26, str, 1)

    assert isinstance(custom_stream2, custom_stream_class)
