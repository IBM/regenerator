from regenerator import Stream

def validate_stream(stream, length, item_type, item_length=None):
    assert isinstance(stream, Stream)
    assert len(stream) == length
    assert sum(1 for _ in stream) == length

    for item in stream:
        assert isinstance(item, item_type)
        if item_length is not None:
            assert len(item) == item_length

def test_len(list_stream, number_stream, name_stream):
    assert len(list_stream) == 10
    assert len(number_stream) == 256
    assert len(name_stream) == 4

def test_is_lazy(counter_stream):
    for count, item in enumerate(counter_stream):
        assert counter_stream.generator_func.it == count

def test_batch(number_stream):
    batch_stream = number_stream.batch(10)
    validate_stream(batch_stream, 26, tuple)
    assert max(map(len, batch_stream)) == 10

    batch_list = list(batch_stream)

    assert batch_list[0] == ('199', '197', '12', '228', '185', '149', '219', '246', '244', '238',)
    assert len(batch_list[-1]) == 6

def test_chunk():
    assert Stream.batch is Stream.chunk

def test_batch_empty(empty_stream):
    batch_stream = empty_stream.batch(10)
    assert len(list(batch_stream)) == 0

def test_batch_is_lazy(counter_stream):
    stream = counter_stream.batch(2)
    for count, item in enumerate(stream):
        assert counter_stream.generator_func.it == count * 2 + 1

def test_chain(name_stream, number_stream):
    chain_stream = Stream.chain(name_stream, number_stream, name_stream)
    validate_stream(chain_stream, 4 + 256 + 4, str)

    chain_stream = name_stream.chain(number_stream, name_stream)
    validate_stream(chain_stream, 4 + 256 + 4, str)

    chain_stream = name_stream + number_stream + name_stream
    validate_stream(chain_stream, 4 + 256 + 4, str)

    list_stream = list(chain_stream)
    assert list_stream[0] == 'Elliott 38'
    assert list_stream[-1] == 'Alexa 3'

def test_chain_empty(empty_stream, name_stream):
    chain_stream = empty_stream + empty_stream
    assert len(list(chain_stream)) == 0

    chain_stream = name_stream.chain()
    assert len(chain_stream) == len(name_stream) == 4

def test_chain_is_lazy(counter_stream, counter_stream2):
    chain_stream = counter_stream.chain(counter_stream2)

    for count, item in enumerate(chain_stream):
        if count < 10:
            assert count == counter_stream.generator_func.it
        else:
            assert (count - 10) == counter_stream2.generator_func.it
