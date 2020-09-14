from regenerator import Stream

from .util import *

def test_is_lazy(counter_stream):
    for count, item in enumerate(counter_stream):
        assert counter_stream.generator_func.it == count
