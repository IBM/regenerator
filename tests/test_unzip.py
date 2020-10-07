import random

import pytest

from regenerator import Stream

from .util import *

def test_unzip(zipped_stream):
    integer_stream, real_stream, character_stream = zipped_stream.unzip()
    validate_stream(integer_stream, 10, int)
    validate_stream(real_stream, 10, float)
    validate_stream(character_stream, 10, str)

def test_zip_unzip(name_stream, number_stream):
    zipped_stream = name_stream.zip(number_stream)
    validate_stream(zipped_stream, 4, tuple)

    name_stream, number_stream = zipped_stream.unzip()
    name_stream = name_stream.map(str.split)
    validate_stream(name_stream, 4, list, 2)
    validate_stream(number_stream, 4, str)

def test_unzip_n(zipped_stream):
    integer_stream, real_stream, character_stream = zipped_stream.unzip(n=3)
    validate_stream(integer_stream, 10, int)
    validate_stream(real_stream, 10, float)
    validate_stream(character_stream, 10, str)

def test_unzip_small_n(zipped_stream):
    integer_stream, real_stream = zipped_stream.unzip(2)
    validate_stream(integer_stream, 10, int)
    validate_stream(real_stream, 10, float)

def test_unzip_big_n(zipped_stream):
    with pytest.raises(ValueError):
        integer_stream, real_stream, character_stream = zipped_stream.unzip(n=4)

    streams = zipped_stream.unzip(n=4)
    with pytest.raises(IndexError):
        list(streams[-1])

def test_empty_stream(empty_stream):
    with pytest.raises(ValueError):
        integer_stream, real_stream, character_stream = empty_stream.unzip()

    integer_stream, real_stream, character_stream = empty_stream.unzip(3)
    validate_stream(integer_stream, 0, int)
    validate_stream(real_stream, 0, float)
    validate_stream(character_stream, 0, str)

def test_is_lazy(counter_stream, counter_stream2):
    zipped_stream = counter_stream.zip(counter_stream2)
    unzipped_stream1, unzipped_stream2 = zipped_stream.unzip(2)
    validate_stream(unzipped_stream1, 10, int)
    validate_stream(unzipped_stream2, 10, int)

    for count, item in enumerate(unzipped_stream1):
        assert item == count
        assert counter_stream.generator_func.it == count

    for count, item in enumerate(unzipped_stream2):
        assert item == count
        assert counter_stream2.generator_func.it == count

def test_custom_type(custom_stream, custom_stream_class):
    zipped_stream = custom_stream.zip(custom_stream)
    unzipped_stream1, unzipped_stream2 = zipped_stream.unzip(2)

    validate_stream(unzipped_stream1, 24, int)
    assert isinstance(unzipped_stream1, custom_stream_class)

    validate_stream(unzipped_stream2, 24, int)
    assert isinstance(unzipped_stream2, custom_stream_class)
