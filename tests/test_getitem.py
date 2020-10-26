import pytest

from regenerator import Stream

from .util import *

def test_getitem_idx(list_stream):
    item = list_stream[3]
    assert item == 3

def test_negative_idx(list_stream):
    with pytest.raises(IndexError):
        list_stream[-1]

def test_str_idx(list_stream):
    with pytest.raises(TypeError):
        list_stream['junk']

def test_idx_out_of_range(list_stream):
    with pytest.raises(IndexError):
        list_stream[100_000]

def test_slice(list_stream):
    slice_stream = list_stream[2:4]
    validate_stream(slice_stream, 2, int)

def test_empty(empty_stream):
    with pytest.raises(IndexError):
        empty_stream[0]

def test_custom_type(custom_stream, custom_stream_class):
    slice_stream = custom_stream[:10]
    validate_stream(slice_stream, 10, int)

    assert isinstance(slice_stream, custom_stream_class)
