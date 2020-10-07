from regenerator import Stream

from .util import *

def test_batch(number_stream):
    batched_stream = number_stream.batch(10)
    validate_stream(batched_stream, 26, tuple)
    assert max(map(len, batched_stream)) == 10

    batched_list = list(batched_stream)
    assert batched_list[0] == ('199', '197', '12', '228', '185', '149', '219', '246', '244', '238',)
    assert len(batched_list[-1]) == 6

def test_chunk():
    assert Stream.chunk is Stream.batch

def test_empty(empty_stream):
    batched_stream = empty_stream.batch(10)
    validate_stream(batched_stream, 0, tuple)

def test_is_lazy(counter_stream):
    stream = counter_stream.batch(2)
    for count, item in enumerate(stream):
        assert counter_stream.generator_func.it == count * 2 + 1

def test_custom_type(custom_stream, custom_stream_class):
    batched_stream = custom_stream.batch(2)
    validate_stream(batched_stream, 12, tuple)

    assert isinstance(batched_stream, custom_stream_class)
