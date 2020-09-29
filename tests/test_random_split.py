import random

import pytest

from regenerator import Stream

from .util import *

def test_split_half(list_stream):
    train_stream, test_stream = list_stream.random_split(0.5, seed=1234)

    validate_stream(train_stream, 4, int)
    validate_stream(test_stream, 6, int)

def test_rand_seed(list_stream):
    train_stream, test_stream = list_stream.random_split(0.2)

    # closures over three variables, seed, frac and self
    train_closure_values = [cell.cell_contents for cell in train_stream.generator_func.__closure__]
    assert len(train_closure_values) == 3
    assert any([isinstance(val, int) for val in train_closure_values]) # seed
    assert any([isinstance(val, float) for val in train_closure_values]) # frac
    assert any([isinstance(val, Stream) for val in train_closure_values]) # self

    test_closure_values = [cell.cell_contents for cell in test_stream.generator_func.__closure__]
    assert len(test_closure_values) == 3
    assert any([isinstance(val, int) for val in test_closure_values]) # seed
    assert any([isinstance(val, float) for val in test_closure_values]) # frac
    assert any([isinstance(val, Stream) for val in test_closure_values]) # self

    # verify that the two seeds are the same
    for train_val in train_closure_values:
        for test_val in test_closure_values:
            if isinstance(train_val, int) and isinstance(test_val, int):
                assert train_val == test_val

def test_empty_stream(empty_stream):
    train_stream, test_stream = empty_stream.random_split()
    validate_stream(train_stream, 0, object)
    validate_stream(test_stream, 0, object)

def test_zero_frac(name_stream):
    train_stream, test_stream = name_stream.random_split(0.0)
    validate_stream(train_stream, 0, str)
    validate_stream(test_stream, 4, str)

def test_unit_frac(name_stream):
    train_stream, test_stream = name_stream.random_split(1.0)
    validate_stream(train_stream, 4, str)
    validate_stream(test_stream, 0, str)

def test_invalid_frac(name_stream):
    with pytest.raises(ValueError):
        train_stream, test_stream = name_stream.random_split(42.0)

def test_is_lazy(counter_stream):
    train_stream, test_stream = counter_stream.random_split(frac=1.0, seed=102)
    validate_stream(train_stream, 10, int)
    validate_stream(test_stream, 0, int)

    for count, item in enumerate(train_stream):
        assert item == count
        counter_stream.generator_func.it == count

    train_stream, test_stream = counter_stream.random_split(frac=0.0, seed=102)
    validate_stream(train_stream, 0, int)
    validate_stream(test_stream, 10, int)

    for count, item in enumerate(test_stream):
        assert item == count
        counter_stream.generator_func.it == count

def test_custom_type(custom_stream, custom_stream_class):
    train_stream, test_stream = custom_stream.random_split(seed=100)
    validate_stream(train_stream, 13, int)
    validate_stream(test_stream, 11, int)

    assert isinstance(train_stream, custom_stream_class)
    assert isinstance(test_stream, custom_stream_class)
