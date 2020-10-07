import os, string
import pytest

import regenerator

basedir = os.path.dirname(__file__)

@pytest.fixture
def list_stream():
    return regenerator.Stream.from_iterable(list(range(10)))

@pytest.fixture
def names_path():
    return os.path.join(basedir, 'data', 'names.txt')

@pytest.fixture
def name_stream(names_path):
    return regenerator.Stream.from_txt(names_path).map(lambda item: item.rstrip())

@pytest.fixture
def numbers_path():
    return os.path.join(basedir, 'data', 'numbers.txt')

@pytest.fixture
def number_stream(numbers_path):
    return regenerator.Stream.from_txt(numbers_path).map(lambda item: item.rstrip())

@pytest.fixture
def batched_stream():
    return regenerator.Stream.from_func(lambda: (tuple(range(i, i+10)) for i in range(0, 100, 10)))

@pytest.fixture
def zipped_stream():
    return regenerator.Stream.from_func(
        lambda: ((integer, integer / 3.14159, character)
            for integer, character in zip(range(10), string.ascii_lowercase)))

@pytest.fixture
def empty_stream():
    return regenerator.Stream.from_iterable(())

@pytest.fixture
def counter_stream():
    def generator_func():
        generator_func.it = 0
        for i in range(10):
            yield i
            generator_func.it += 1

    return regenerator.Stream(generator_func)

@pytest.fixture
def counter_stream2():
    def generator_func():
        generator_func.it = 0
        for i in range(10):
            yield i
            generator_func.it += 1

    return regenerator.Stream(generator_func)

class CustomStream(regenerator.Stream):
    def __init__(self, n=24):
        super().__init__(lambda: iter(range(n)))

    @regenerator.newstream
    def even(cls, self):
        return cls.from_func(lambda: (item for item in self if item % 2 == 0))

    @regenerator.newstream
    def increment(cls, self):
        return cls.from_func(lambda: (item + 1 for item in self))

@pytest.fixture
def custom_stream():
    return CustomStream()

@pytest.fixture
def custom_stream_class():
    return CustomStream
