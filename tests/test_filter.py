from regenerator import Stream

from .util import *

def test_filter_small(number_stream):
    number_stream = number_stream.map(int)

    small_stream = number_stream.filter(lambda item: item < 10)

    validate_stream(small_stream, 10, int)

    assert min(small_stream) == 0
    assert max(small_stream) == 9

def test_no_func():
    none_stream = Stream.from_iterable([1, 2, None, 3, 4, None, 5])
    validate_stream(none_stream, 7, (int, type(None)))

    filter_stream = none_stream.filter()
    validate_stream(filter_stream, 5, int)

def test_empty(empty_stream):
    filter_stream = empty_stream.filter(lambda item: item)
    validate_stream(filter_stream, 0, object)

def test_is_lazy(counter_stream):
    filter_stream = counter_stream.filter(lambda item: item >= 5)
    validate_stream(filter_stream, 5, int)

    for count, item in enumerate(filter_stream, 5):
        assert count == counter_stream.generator_func.it

def test_custom_type(custom_stream, custom_stream_class):
    filter_stream = custom_stream.filter(lambda item: item < 20)
    validate_stream(filter_stream, 20, int)

    assert isinstance(filter_stream, custom_stream_class)
