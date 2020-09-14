import string, tempfile

from regenerator import Stream

from .util import *

def test_from_txt(names_path):
    txt_stream = Stream.from_txt(names_path)
    validate_stream(txt_stream, 4, str)

def test_from_empty_txt():
    '''Validate that loading an empty file results in an empty stream.
    '''
    # create a stream from an empty temp file and validate that its empty
    with tempfile.NamedTemporaryFile() as temp_file:
        txt_stream = Stream.from_txt(temp_file.name)
        validate_stream(txt_stream, 0, object)

def test_custom_type(custom_stream, custom_stream_class, numbers_path):
    custom_stream2 = custom_stream_class.from_txt(numbers_path)
    validate_stream(custom_stream2, 256, str)

    assert isinstance(custom_stream2, custom_stream_class)
