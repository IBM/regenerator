import pytest

from regenerator import Stream

from .util import *

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

def test_no_args(empty_stream):
    validate_stream(empty_stream.chain(), 0, object)

    with pytest.raises(TypeError):
        Stream.chain()

def test_empty(empty_stream, name_stream):
    chain_stream = empty_stream + empty_stream
    assert len(list(chain_stream)) == 0

    chain_stream = name_stream.chain()
    assert len(chain_stream) == len(name_stream) == 4

def test_is_lazy(counter_stream, counter_stream2):
    chain_stream = counter_stream.chain(counter_stream2)
    validate_stream(chain_stream, 20, int)

    for count, item in enumerate(chain_stream):
        if count < 10:
            assert count == counter_stream.generator_func.it
        else:
            assert (count - 10) == counter_stream2.generator_func.it

def test_custom_type(custom_stream, custom_stream_class):
    chain_stream = custom_stream.chain(custom_stream)
    validate_stream(chain_stream, 48, int)

    assert isinstance(chain_stream, custom_stream_class)
