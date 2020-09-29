import random

import pytest

from regenerator import Stream

from .util import *

def test_split2(list_stream):
    train_stream, test_stream = list_stream.split(2)

    validate_stream(train_stream, 5, int)
    validate_stream(test_stream, 5, int)

    for item, idx in zip(train_stream, range(0, 10, 2)):
        assert item == idx

    for item, idx in zip(test_stream, range(1, 10, 2)):
        assert item == idx

def test_split3(list_stream):
    streams = list_stream.split(3)
    train_stream, valid_stream, test_stream = streams

    validate_stream(train_stream, 4, int)
    validate_stream(valid_stream, 3, int)
    validate_stream(test_stream, 3, int)

    for i, stream in enumerate(streams):
        for item, idx in zip(stream, range(i, 10, 3)):
            assert item == idx

def test_empty_stream(empty_stream):
    train_stream, test_stream = empty_stream.split()
    validate_stream(train_stream, 0, object)
    validate_stream(test_stream, 0, object)

def test_zero(name_stream):
    streams = name_stream.split(0)
    assert len(streams) == 0

def test_one(name_stream):
    streams = name_stream.split(1)
    assert len(streams) == 1
    validate_stream(streams[0], 4, str)

def test_is_lazy(counter_stream):
    train_stream, test_stream = counter_stream.split(2)
    validate_stream(train_stream, 5, int)
    validate_stream(test_stream, 5, int)

    for count, item in enumerate(train_stream):
        assert item == 2 * count
        assert counter_stream.generator_func.it == 2 * count

    for count, item in enumerate(test_stream):
        assert item == 2 * count + 1
        assert counter_stream.generator_func.it == 2 * count + 1

def test_custom_type(custom_stream, custom_stream_class):
    train_stream, test_stream = custom_stream.split(2)
    validate_stream(train_stream, 12, int)
    validate_stream(test_stream, 12, int)

    assert isinstance(train_stream, custom_stream_class)
    assert isinstance(test_stream, custom_stream_class)
