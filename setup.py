#!/usr/bin/env python
import os, setuptools

version = '0.2.0'

basedir = os.path.dirname(__file__)
with open(os.path.join(basedir, 'README.md')) as fh:
    long_description = fh.read()

with open(os.path.join(basedir, 'LICENSE')) as fh:
    license = fh.read()

setuptools.setup(
    name='regenerator',
    version=version,
    author='IBM / Elliott Forney',
    author_email='elliott.forney@gmail.com',
    description='ReGenerator a reentrant generator streams for lazy data processing.',
    license=license,
    url='https://github.com/ibm/regenerator',
    packages=('regenerator',),
    long_description=long_description,
)
