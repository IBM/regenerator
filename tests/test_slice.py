import pytest

from regenerator import Stream

from .util import *

def test_slice_first(list_stream):
    slice_stream = list_stream.slice(0, 5, 2)
    validate_stream(slice_stream, 3, int)

def test_no_args(name_stream):
    with pytest.raises(TypeError):
        slice_stream = name_stream.slice()
        list(slice_stream)

def test_constant_slice(list_stream):
    slice_stream = list_stream.slice(3)
    assert list(slice_stream) == [0, 1, 2]

def test_empty_slice(name_stream):
    slice_stream = name_stream.slice(0)
    validate_stream(slice_stream, 0, int)

def test_empty(empty_stream):
    slice_stream = empty_stream.slice(2)
    validate_stream(slice_stream, 0, object)

def test_is_lazy(counter_stream):
    slice_stream = counter_stream.slice(5)
    validate_stream(slice_stream, 5, int)

    for count, item in enumerate(slice_stream):
        assert item == count
        assert count == counter_stream.generator_func.it

def test_custom_type(custom_stream, custom_stream_class):
    slice_stream = custom_stream.slice(10)
    validate_stream(slice_stream, 10, int)

    assert isinstance(slice_stream, custom_stream_class)
