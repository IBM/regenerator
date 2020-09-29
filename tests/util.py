from regenerator import Stream

def validate_stream(stream, length, item_type, item_length=None):
    '''Validate that a stream has the specified length, item type, and (optional) item length.
    '''
    assert isinstance(stream, Stream), '{} not a stream'.format(type(stream).__name__)
    assert len(stream) == length, 'unexpected length {} != {}'.format(len(stream), length)

    computed_len = sum(1 for _ in stream)
    assert computed_len == length, \
        'unexpected computed length {} != {}'.format(computed_len, length)

    for item in stream:
        assert isinstance(item, item_type), \
            'unexpected item type {} != {}'.format(type(item).__name__, item_type.__name__)
        if item_length is not None:
            assert len(item) == item_length, \
                'unexpected item length {} != {}'.format(len(item), item_length)
