import random

import pytest

from regenerator import Stream

from .util import *

def test_column(zipped_stream):
    integer_stream = zipped_stream.column(0)
    real_stream = zipped_stream.col(1)
    character_stream = zipped_stream.column(2)

    validate_stream(integer_stream, 10, int)
    validate_stream(real_stream, 10, float)
    validate_stream(character_stream, 10, str)

def test_empty_stream(empty_stream):
    column_stream = empty_stream.column(0)
    validate_stream(column_stream, 0, int)

def test_is_lazy(counter_stream, counter_stream2):
    zipped_stream = counter_stream.zip(counter_stream2)

    column_stream1 = zipped_stream.column(0)
    column_stream2 = zipped_stream.col(1)

    validate_stream(column_stream1, 10, int)
    validate_stream(column_stream2, 10, int)

    for count, item in enumerate(column_stream1):
        assert item == count
        assert counter_stream.generator_func.it == count

    for count, item in enumerate(column_stream2):
        assert item == count
        assert counter_stream2.generator_func.it == count

def test_custom_type(custom_stream, custom_stream_class):
    zipped_stream = custom_stream.zip(custom_stream)
    column_stream1 = zipped_stream.col(0)
    column_stream2 = zipped_stream.column(1)

    validate_stream(column_stream1, 24, int)
    assert isinstance(column_stream1, custom_stream_class)

    validate_stream(column_stream2, 24, int)
    assert isinstance(column_stream2, custom_stream_class)
