from regenerator import Stream

from .util import *

def test_batch(number_stream):
    batch_stream = number_stream.batch(10)
    validate_stream(batch_stream, 26, tuple)
    assert max(map(len, batch_stream)) == 10

    batch_list = list(batch_stream)
    assert batch_list[0] == ('199', '197', '12', '228', '185', '149', '219', '246', '244', '238',)
    assert len(batch_list[-1]) == 6

def test_chunk():
    assert Stream.batch is Stream.chunk

def test_empty(empty_stream):
    batch_stream = empty_stream.batch(10)
    validate_stream(batch_stream, 0, tuple)

def test_is_lazy(counter_stream):
    stream = counter_stream.batch(2)
    for count, item in enumerate(stream):
        assert counter_stream.generator_func.it == count * 2 + 1

def test_custom_type(custom_stream, custom_stream_class):
    batch_stream = custom_stream.batch(2)
    validate_stream(batch_stream, 12, tuple)

    assert isinstance(batch_stream, custom_stream_class)
