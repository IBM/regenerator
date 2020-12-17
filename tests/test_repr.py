import pytest
import string

from regenerator import Stream

from .util import *

def validate_header(stream_repr, class_name=Stream.__name__):
    return stream_repr.startswith(f'<{class_name}>:')

def test_few_short():
    stream = Stream.from_iterable(range(3))
    validate_stream(stream, 3, int)

    stream_repr = repr(stream)
    validate_header(stream_repr)
    assert ', ' in stream_repr
    assert not stream_repr.endswith('...')

def test_many_short():
    stream = Stream.from_iterable(range(100))
    validate_stream(stream, 100, int)

    stream_repr = repr(stream)
    validate_header(stream_repr)
    assert ', ' in stream_repr
    assert stream_repr.endswith('...')

def test_few_long():
    long_string = string.ascii_letters * 2

    stream = Stream.from_iterable([long_string,] * 3)
    validate_stream(stream, 3, str, len(long_string))

    stream_repr = repr(stream)
    validate_header(stream_repr)
    assert ',\n' in stream_repr
    assert not stream_repr.endswith('...')

def test_many_long():
    long_string = string.ascii_letters * 2

    stream = Stream.from_iterable([long_string,] * 100)
    validate_stream(stream, 100, str, len(long_string))

    stream_repr = repr(stream)
    validate_header(stream_repr)
    assert ',\n' in stream_repr
    assert stream_repr.endswith('...')

def test_empty(empty_stream):
    assert validate_header(repr(empty_stream))
