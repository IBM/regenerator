import os
import pytest
import regenerator

basedir = os.path.dirname(__file__)

@pytest.fixture
def list_stream():
    return regenerator.Stream.from_iterable(list(range(10)))

@pytest.fixture
def name_stream():
    return regenerator.Stream.from_txt(
        os.path.join(basedir, 'data', 'names.txt')).map(lambda item: item.rstrip())

@pytest.fixture
def number_stream():
    return regenerator.Stream.from_txt(
        os.path.join(basedir, 'data', 'numbers.txt')).map(lambda item: item.rstrip())

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
