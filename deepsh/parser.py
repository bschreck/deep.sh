"""Implements the deepsh parser."""

from deepsh.lib.lazyasd import lazyobject
from deepsh.platform import PYTHON_VERSION_INFO


@lazyobject
def Parser():
    if PYTHON_VERSION_INFO >= (3, 13):
        from deepsh.parsers.v313 import Parser as p
    elif PYTHON_VERSION_INFO > (3, 10):
        from deepsh.parsers.v310 import Parser as p
    elif PYTHON_VERSION_INFO > (3, 9):
        from deepsh.parsers.v39 import Parser as p
    elif PYTHON_VERSION_INFO > (3, 8):
        from deepsh.parsers.v38 import Parser as p
    else:
        from deepsh.parsers.v36 import Parser as p
    return p
