import random

import pytest

from regenerator import Stream

from .util import *

def test_zip(name_stream, number_stream):
    zipped_stream = name_stream.zip(number_stream)
    validate_stream(zipped_stream, 4, tuple)

def test_empty_stream(empty_stream):
    zipped_stream = empty_stream.zip(empty_stream)
    validate_stream(zipped_stream, 0, int)

def test_is_lazy(counter_stream, counter_stream2):
    zipped_stream = counter_stream.zip(counter_stream2)
    validate_stream(zipped_stream, 10, tuple)

    for count, (item1, item2) in enumerate(zipped_stream):
        assert count == item1
        assert count == item2
        assert counter_stream.generator_func.it == count
        assert counter_stream2.generator_func.it == count

def test_custom_type(custom_stream, custom_stream_class):
    zipped_stream = custom_stream.zip(custom_stream)
    validate_stream(zipped_stream, 24, tuple)
    assert isinstance(zipped_stream, custom_stream_class)
