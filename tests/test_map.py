import pytest

from regenerator import Stream

from .util import *

def test_map_int_add(number_stream):
    number_stream = number_stream.map(int).map(lambda item: item + 10)

    validate_stream(number_stream, 256, int)

    assert min(number_stream) == 10
    assert max(number_stream) == (255 + 10)

def test_no_func(name_stream):
    with pytest.raises(TypeError):
        name_stream.map()

def test_empty(empty_stream):
    map_stream = empty_stream.map(len)
    validate_stream(map_stream, 0, object)

def test_is_lazy(counter_stream):
    map_stream = counter_stream.map(lambda item: item * 10)
    validate_stream(map_stream, 10, int)

    for count, item in enumerate(map_stream):
        assert item == count * 10
        assert count == counter_stream.generator_func.it

def test_custom_type(custom_stream, custom_stream_class):
    map_stream = custom_stream.map(float).map(lambda item: item / 2)
    validate_stream(map_stream, 24, float)

    assert isinstance(map_stream, custom_stream_class)
