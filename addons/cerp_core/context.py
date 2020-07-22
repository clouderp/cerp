# -*- coding: utf-8 -*-

import os
import tempfile
from contextlib import contextmanager


@contextmanager
def secretenv(**kwargs):
    for k in kwargs:
        os.environ[k] = kwargs[k]
    try:
        yield
    finally:
        for k in kwargs:
            del os.environ[k]


@contextmanager
def secretfile(secrets, filename='secrets.txt'):
    with tempfile.TemporaryDirectory() as tmpdirname:
        path = os.path.join(tmpdirname, filename)
        with open(path, 'w') as f:
            f.write(secrets)
        yield path
