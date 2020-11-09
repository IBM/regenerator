'''Reentrant generator (ReGenerator) stream.'''
import functools, itertools, random

def newstream(func):
    '''Decorator for methods that return new stream instances.  First argument is the
    class so that streams can play nicely with inheritance and second argument is self so
    that member attributes can be accessed.
    '''
    @functools.wraps(func)
    def wrapped(self, *args, **kwargs):
        return func(self.__class__, self, *args, **kwargs)
    return wrapped

class Stream:
    '''A ReGenerator `Stream` is an iterable container class that is designed to permit
    lazy processing of data in a streaming fashion.  The data items produced by a stream
    can be any python object.  In addition to being lazily evaluated, like ordinary python
    generators and iterators, streams are also reentrant in the sense that they can be
    iterated over multiple times.  This is achieved via a generator function, which is the
    sole argument to the class `.__init__` method, that reconstructs a python iterator or
    generator each time it is called.

    Streams provide a number of convenience methods, including functional-style operations,
    for manipulating, filtering and combining streams in fast, generic and straightforward
    ways.  Streams are also extensible and simple extension of the stream class allows
    new functionality to be added.
    '''
    def __init__(self, generator_func):
        '''Construct a new reentrant generator stream.  The `generator_func` function is
        called each time an iterator over the stream is created, allowing for repeated
        lazy iteration.  Note that you may want to consider using one of the provided
        class method in order to construct a new stream before writing your own generator
        function.
        '''
        self._init(generator_func)

    def _init(self, generator_func):
        '''Initialize a new stream from a generator function.  This is outside of the
        constructor so that it can also be called by `from_func`.  This is for internal
        use only and allows new streams to be initialized from outside of the constructor.
        '''
        self.generator_func = generator_func
        return self

    #### initializers ####

    @classmethod
    def from_func(cls, generator_func):
        '''Construct a new stream from the provided generator function.  When adding
        methods to the stream class (including on subclasses) that return new streams,
        this classmethod should be used instead of calling the constructor directly.
        The allows subclasses to override the constructor without breaking these methods.
        '''
        # pylint: disable=protected-access
        return cls.__new__(cls)._init(generator_func)

    @classmethod
    def from_iterable(cls, data):
        '''Create a new stream from a python iterable, generally a sequence like a list or
        a tuple.  Note that `data` can be pretty much anything you can pass as an argument
        to the `iter` builtin as long as it can be iterated over *multiple times*.  If
        iterating over `data` exhausts the underlying elements, e.g., for the result of
        calling `open`, then your stream will become empty after the first time it is
        iterated over.
        '''
        return cls.from_func(lambda: iter(data))

    @classmethod
    def from_txt(cls, filename, *args, **kwargs):
        '''Create a new stream from the lines of a text file.  Each line of the file will
        become an item in the created stream, including blank lines.  `*args` and `**kwargs`
        are passed to the `open` function.
        '''
        def generator_func():
            with open(filename, mode='r', *args, **kwargs) as fh:
                for line in fh:
                    yield line

        return cls.from_func(generator_func)

    #### modifiers ####

    @newstream
    def batch(cls, self, size):
        '''Combine `size` adjacent elements of together into tuples.  This process is often
        called batching or chunking.
        '''
        def generator_func():
            it = iter(self)
            return iter(lambda: tuple(itertools.islice(it, size)), ())

        return cls.from_func(generator_func)

    # alias for batch
    chunk = batch

    @newstream
    def chain(cls, self, *args):
        '''Chain multiple streams together sequentially, i.e., return the elements of
        the first stream in `args` followed by the elements in the second stream, et cetra.
        This is analogous to the `itertools.chain` function.
        '''
        return cls.from_func(lambda: itertools.chain(self, *args))

    @newstream
    def fix(cls, self):
        '''Evaluate the stream and place all items it contains into memory.  This process
        "fixes" the stream at the current point in time.  This may improve computational
        performance because the stream will no longer be lazily evaluated on demand.
        Beware, however, that this may consume large amounts of memory for large streams.
        '''
        return cls.from_iterable(tuple(self))

    eager = fix

    @newstream
    def filter(cls, self, func=None):
        '''Keep only items in the stream where `func(item)` evaluates to `True`.
        If `None` (default) then `None` values will be removed.  This is analogous to the
        standard python `filter` function.
        '''
        return cls.from_func(lambda: filter(func, self))

    @newstream
    def map(cls, self, func):
        '''Apply `func` to each element in the stream.  This is analogous to the standard
        python `map` function.
        '''
        return cls.from_func(lambda: map(func, self))

    @newstream
    def slice(cls, self, *args, **kwargs):
        '''Slice the items in the stream by `stop` or `start, stop[, step]`.  This is
        analogous to the `iterstreams.islice` function.  Note: slicing large streams may
        be very slow since all items before and in between the retrieved slices must be
        processed.
        '''
        return cls.from_func(lambda: itertools.islice(self, *args, **kwargs))

    @newstream
    def random_split(cls, self, frac=0.5, seed=None):
        '''Split the stream into two new streams with randomly selected elements randomly
        with probability of `frac` of being placed in the first stream and `1.0 - frac` of
        being placed in the second stream.  Note that the same random seed is used when
        iterating over the stream, so the same split will be generated when iterating over
        the stream multiple times.  The `seed` argument can be used to manually specify
        the integer random seed to use.  If `seed=None` (default) then a random seed will
        be selected from the range [0, 1_000_000].
        '''
        if not 0.0 <= frac <= 1.0:
            raise ValueError('invalid frac `{}` not in [0, 1]'.format(frac))

        if seed is None:
            seed = random.randint(0, 1_000_000)

        def generator_func_a():
            rng = random.Random(seed)
            return (item for item in self if rng.random() <= frac)

        def generator_func_b():
            rng = random.Random(seed)
            return (item for item in self if rng.random() > frac)

        return cls.from_func(generator_func_a), cls.from_func(generator_func_b)

    @newstream
    def split(cls, self, n=2):
        '''Split the stream into `n` streams with items being placed in each stream in a
        round robin fashion.
        '''
        def select_func(i):
            return (item for j, item in enumerate(self) if ((j-i) % n) == 0)

        return tuple(cls.from_func(functools.partial(select_func, i)) for i in range(n))

    @newstream
    def unbatch(cls, self):
        '''Assume that each item in the stream is a sequence, e.g., tuples or lists, and
        yield each subitem.  This unnests a stream of sequences and is the inverse of
        `.batch` and `.chunk`.
        '''
        return cls.from_func(lambda: (subitem for item in self for subitem in item))

    # alias for unbatch
    unchunk = unbatch

    @newstream
    def unzip(cls, self, n=None):
        '''Assume that the items in the stream are sequences, i.e., tuples or lists, with
        equal length and separate / unzip the stream into a tuple of separate streams.
        This is the inverse of `.zip` and is analogous to `zip(*zipped_sequence)` when
        working with regular python iterators.

        The argument `n` specifies the number of elements to expect in each data item.
        If `n` is `None` (default) then `n` will be set to the length of the first item in
        the stream.  Note that an empty stream will raise a `ValueError` because it is not
        possible to infer the length of the data items.  If an item in the stream has a
        length that is greater than `n` it will be truncated.  If an item has length less
        than `n` then an `IndexError` will be raised at runtime.
        '''
        if n is None:
            try:
                n = len(next(iter(self)))
            except StopIteration:
                # pylint: disable=raise-missing-from
                raise ValueError('cannot infer length of items from empty stream')

        def select_func(i):
            return (item[i] for item in self)

        return tuple(cls.from_func(functools.partial(select_func, i)) for i in range(n))

    @newstream
    def column(cls, self, idx):
        '''Assume that the items in the stream can be indexed via `.__getitem__`, e.g.,
        for tuples or lists, and return a stream that selects the subitem at the `idx`'th
        position for each item in the stream.  In other words, create a new stream that
        yields the column with index `idx`.
        '''
        return cls.from_func(lambda: (item[idx] for item in self))

    # alias for column
    col = column

    @newstream
    def zip(cls, self, *args):
        '''Zip the elements of multiple streams together so that each item in the resulting
        stream is a tuple of items from each of the zipped streams.  This is analogous to
        the standard python `zip` function.  Note, the shortest of the zipped streams will
        determine the length of the resulting stream.
        '''
        return cls.from_func(lambda: zip(self, *args))

    @newstream
    def zip_longest(cls, self, *args, fillvalue=None):
        '''Zip the elements of multiple streams together, similar to the `.zip` method,
        except that the longest of the zipped streams will determine the length of the
        resulting stream and the value of the argument `fillvalue` will be used to pad
        shorter streams.  This is analogous to the `itertools.zip_longest` function.
        '''
        return cls.from_func(lambda: itertools.zip_longest(self, *args, fillvalue=fillvalue))

    #### magic functions ####

    def __add__(self, other):
        '''The addition operator for streams is equivalent to chaining the streams together
        with the `.chain` method.
        '''
        return self.chain(other)

    @newstream
    def __getitem__(cls, self, idx):
        '''Index or slice into the stream.  If `idx` is a slice, then a list containing
        the sliced elements is returned.  If `idx` is an integer, then the sole element
        located at the provided index will be returned.  Note that these operations may
        be slow since all elements in the stream must be iterated over until the desired
        items are found.  Negative indexing is not supported.  If want to create a stream
        over a slice, instead of a list, consider using the `slice` method instead.
        '''
        # pylint: disable=unexpected-special-method-signature
        if isinstance(idx, slice):
            return list(self.slice(idx.start, idx.stop, idx.step))

        if not isinstance(idx, int):
            raise TypeError('indices must be integers or slices, not {}'.format(type(idx).__name__))

        if idx < 0:
            raise IndexError('negative indexing not supported')

        for i, item in enumerate(self):
            if i == idx:
                return item

        raise IndexError('stream index out of range')

    def __iter__(self):
        '''A new iterator for the stream is created by calling `generator_func`.
        '''
        return self.generator_func()

    def __len__(self):
        '''Get the number of elements contained in this stream.  Note that this requires
        the entire stream to be iterated over, and so can be slow for large streams.
        '''
        return sum(1 for _ in self)
