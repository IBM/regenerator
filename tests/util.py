from regenerator import Stream

def validate_stream(stream, length, item_type, item_length=None):
    '''Validate that a stream has the specified length, item type, and (optional) item length.
    '''
    assert isinstance(stream, Stream), 'Not a stream.'
    assert len(stream) == length, 'Unexpected length.'
    assert sum(1 for _ in stream) == length, 'Unexpected length computed.'

    for item in stream:
        assert isinstance(item, item_type), 'Unexpected item type.'
        if item_length is not None:
            assert len(item) == item_length, 'Unexpected item length.'
