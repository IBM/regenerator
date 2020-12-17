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
    slice_list = list_stream[2:4]

    assert isinstance(slice_list, Stream)
    assert len(slice_list) == 2

def test_empty(empty_stream):
    with pytest.raises(IndexError):
        empty_stream[0]

def test_custom_type(custom_stream, custom_stream_class):
    slice_list = custom_stream[:10]

    assert isinstance(slice_list, custom_stream_class)
    assert len(slice_list) == 10
