from regenerator import Stream

from .util import *

def test_fix(name_stream):
    assert list(name_stream.fix()) == list(name_stream)

def test_is_not_lazy(counter_stream):
    fixed_stream = counter_stream.fix()
    length = len(counter_stream)

    for count, item in enumerate(fixed_stream):
        assert counter_stream.generator_func.it == length

def test_eager():
    assert Stream.fix is Stream.eager

def test_custom_type(custom_stream, custom_stream_class):
    fixed_stream = custom_stream.fix()
    validate_stream(fixed_stream, 24, int)

    assert isinstance(fixed_stream, custom_stream_class)
