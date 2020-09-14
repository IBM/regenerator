'''Verify that test fixtures are as expected.
'''

from regenerator import Stream

from .util import *

def test_list_stream(list_stream):
    validate_stream(list_stream, 10, int)
    assert min(list_stream) == 0
    assert max(list_stream) == 9

def test_name_stream(name_stream):
    validate_stream(name_stream, 4, str)
    assert next(iter(name_stream)) == 'Elliott 38'

def test_number_stream(number_stream):
    validate_stream(number_stream, 256, str)

    int_stream = number_stream.map(int)
    validate_stream(int_stream, 256, int)
    assert min(int_stream) == 0
    assert max(int_stream) == 255

def test_empty_stream(empty_stream):
    validate_stream(empty_stream, 0, object)

def test_counter_stream(counter_stream):
    validate_stream(counter_stream, 10, int)
    for i, item in enumerate(counter_stream):
        assert counter_stream.generator_func.it == i

def test_counter_stream2(counter_stream2):
    validate_stream(counter_stream2, 10, int)
    assert counter_stream2.generator_func.it == 10
    for i, item in enumerate(counter_stream2):
        assert counter_stream2.generator_func.it == i

def test_custom_stream(custom_stream, custom_stream_class):
    assert isinstance(custom_stream, custom_stream_class)

    validate_stream(custom_stream, 24, int)

    even_stream = custom_stream.even()
    assert isinstance(even_stream, custom_stream_class)

    validate_stream(even_stream, 12, int)
    for item in even_stream:
        assert item % 2 == 0

    increment_stream = even_stream.increment()
    assert isinstance(increment_stream, custom_stream_class)

    validate_stream(increment_stream, 12, int)
    for even_item, increment_item in zip(even_stream, increment_stream):
        assert increment_item == (even_item + 1)
