# ReGenerator - Re-Entrant Data Stream Generator

<!-- Insert build status badges here -->
<!-- [![Build Status](https://travis-ci.org/jjasghar/ibm-cloud-cli.svg?branch=master)](https://travis-ci.org/jjasghar/ibm-cloud-cli) -->

ReGenerator, which is short for reentrant generator, is a python package that provides a simple interface for creating lazily evaluated streams of data that can be iterated over multiple times.  In other words, the `regenerator` module provides a container class, called `Stream`, that is both reentrant, i.e., it can be iterated over multiple times and also lazy, i.e., a potential chain of operations on the stream will not actually be computed until the stream is iterated over.  This is achieved by the `Stream` class which is initialized with a "generator function" that recreates a standard python iterator or generator each time it is called.  This class then provides a number of methods with functional-style names, e.g., `zip`, `map`, `slice`, that can be used to perform operations over the stream.  Since these methods also return streams, the entire chain of operations will not actually be performed until the stream is iterated over.

ReGenerator streams can be very useful for creating, munging, cleaning and filtering large amounts of data in data science and machine learning applications.  Since ReGenerator streams are lazily evaluated, they can operate over datasets that are too large to fit into volatile memory.  Since ReGenerator streams are reentrant, they can be used in iterative training algorithms or easily evaluated multiple times during testing and experimentation.  Since ReGenerator streams provide a flexible and extensible design, they can be used to lazily and easily perform a wide variety of custom processing tasks.

## Examples

The [following Jupyter notebook demonstrates the basics of using ReGenerator Streams](examples/regenerator_stream_basics.ipynb).

Here are some applications where ReGenerator streams may be a good fit.

* If you would like to filter out items from a table that is too large to fit into RAM.
```python
from regenerator import Stream

# load a huge csv table from a file
raw_stream = Stream.from_txt('huge_table.csv')

# split the stream by commas
split_stream = raw_stream.map(lambda line: line.strip().split(','))

# keep only lines with 100 entries
clean_stream = split_stream.filter(lambda line: len(line) == 100)

# print each row
for row in clean_stream:
    print(row)
```

* If you would like to apply some preprocessing steps to your data but have those steps change in a nondeterministic way after each iteration, e.g., data augmentation.
```python
from glob import glob

from regenerator import Stream

filenames = glob('images/*.png')

def load_images():
    '''Generator function to load a bunch of images.
    '''
    for filename in filenames:
        yield load_image(filename)

def augment_image(img):
    '''Apply some random data augmentation to an image.
    '''
    img = random_crop(img)
    img = random_rotate(img)
    img = random_scale(img)
    img = random_gamma_correction(img)
    return img

# create a new stream over the images
raw_stream = Stream(load_images)

# apply the data augmentation
# this happens lazily, so this step is very fast
augmented_stream = raw_stream.map(augment_image)

# plot the first image a few times to see the effect
plot_image(augmented_stream[0])
plot_image(augmented_stream[1])
plot_image(augmented_stream[2])

# train some ML or analysis algorithm over the augmented data
model = train(augmented_stream)
```

* If you would like to apply a word tokenizer to __all__ of wikipedia.
```python
import nltk
from regenerator import Stream

# stream over an entire wikipedia dump
# since regenerator streams are lazy, nothing actually
# happends until we iterate over the data
raw_stream = Stream.from_txt('wikipedia_dump.txt')

# strip whitespace and remove blank lines
clean_stream = raw_stream.map(line: line.strip()).filter(lambda line: line)

# create a tokenizer object
tokenizer = nltk.tokenize.WordPunctTokenizer()

# split each line into a list of word tokens
token_stream = clean_stream.map(tokenizer.tokenize)

# pass the tokenized data to an iterative analysis routine
# since it is iterable and reentrant, the algorithm can loop
# over the tokenized lines as many times as it needs
model = train(token_stream)
```

## Installation

To install, point `pip3` directly at GitHub:

```bash
pip3 install 'git+ssh://git@github.com/IBM/regenerator'
```

An official PyPi package will be available in the near future.

## Development

When submitting a pull request, please make sure that the unit tests pass and have 100% coverage:
```bash
pytest -s --cov=regenerator tests
```

Also, please verify that `pylint` passes with a score of 10/10:
```bash
pylint regenerator
```

<!-- License and Authors is optional here, but gives you the ability to highlight who is involed in the project -->
## License & Authors

ReGenerator is provided by IBM under a two-clause BSD license.  For details, please review [the full LICENSE file found here](LICENSE).

- Author: Elliott Forney <Elliott.Forney@ibm.com>
