import random

import pytest

from regenerator import Stream

from .util import *

def test_unbatch(batched_stream):
    unbatched_stream = batched_stream.unbatch()
    validate_stream(unbatched_stream, 100, int)

    assert tuple(range(100)) == tuple(unbatched_stream)

def test_unbatch2(name_stream):
    name_yr_stream = name_stream.map(lambda item: item.rstrip().split())
    validate_stream(name_yr_stream, 4, list, 2)

    unbatched_stream = name_yr_stream.unbatch()
    validate_stream(unbatched_stream, 8, object)

def test_unbatch(number_stream):
    batched_stream = number_stream.batch(3)
    validate_stream(batched_stream, 86, tuple)

    assert Stream.unbatch is Stream.unbatch
    unbatched_stream = batched_stream.unbatch()
    validate_stream(unbatched_stream, 256, str)

    assert tuple(number_stream) == tuple(unbatched_stream)

def test_unchunk():
    assert Stream.unchunk is Stream.unbatch

def test_empty_stream(empty_stream):
    unbatched_stream = empty_stream.unbatch()
    validate_stream(unbatched_stream, 0, object)

def test_empty_tuple_stream():
    empty_tuple_stream = Stream.from_iterable(())
    unbatched_stream = empty_tuple_stream.unbatch()
    validate_stream(unbatched_stream, 0, object)

def test_is_lazy(counter_stream):
    unbatched_stream = counter_stream.batch(2).unbatch()
    validate_stream(unbatched_stream, 10, int)

    for count, item in enumerate(unbatched_stream):
        assert item == count
        assert counter_stream.generator_func.it == 2 * (count // 2) + 1

def test_custom_type(custom_stream, custom_stream_class):
    unbatched_stream = custom_stream.batch(2).unbatch()
    validate_stream(unbatched_stream, 24, int)

    assert isinstance(custom_stream, custom_stream_class)
