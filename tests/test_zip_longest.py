import random

import pytest

from regenerator import Stream

from .util import *

def test_zip_longest(name_stream, number_stream):
    zipped_stream = name_stream.zip_longest(number_stream)
    validate_stream(zipped_stream, 256, tuple)

    zipped_list = list(zipped_stream)
    left, _right = zipped_list[-1]
    assert left == None

def test_fill_value(name_stream, number_stream):
    zipped_stream = number_stream.zip_longest(name_stream, fillvalue=0)
    validate_stream(zipped_stream, 256, tuple)

    zipped_list = list(zipped_stream)
    _left, right = zipped_list[-1]
    assert right == 0

def test_empty_stream(empty_stream):
    zipped_stream = empty_stream.zip_longest(empty_stream)
    validate_stream(zipped_stream, 0, int)

def test_is_lazy(counter_stream, name_stream):
    zipped_stream = counter_stream.zip_longest(name_stream)
    validate_stream(zipped_stream, 10, tuple)

    for count, (item1, item2) in enumerate(zipped_stream):
        assert count == item1
        assert counter_stream.generator_func.it == count

def test_custom_type(name_stream, custom_stream, custom_stream_class):
    zipped_stream = custom_stream.zip_longest(name_stream)
    validate_stream(zipped_stream, 24, tuple)
    assert isinstance(zipped_stream, custom_stream_class)
