"""xontrib tests, such as they are"""
import pytest
from xonsh.xontribs import xontrib_metadata, xontrib_context
import sys

def test_load_xontrib_metadata():
    # Simply tests that the xontribs JSON files isn't malformed.
    xontrib_metadata()

@pytest.yield_fixture
def tmpmod(tmpdir):
    """
    Same as tmpdir but also adds/removes it to the front of sys.path.

    Also cleans out any modules loaded as part of the test.
    """
    sys.path.insert(0, str(tmpdir))
    loadedmods = set(sys.modules.keys())
    try:
        yield tmpdir
    finally:
        del sys.path[0]
        newmods = set(sys.modules.keys()) - loadedmods
        for m in newmods:
            del sys.modules[m]

def test_noall(tmpmod):
    """
    Tests what get's exported from a module without __all__
    """

    with tmpmod.mkdir("xontrib").join("spameggs.py").open('w') as x:
        x.write("""
spam = 1
eggs = 2
_foobar = 3
""")

    ctx = xontrib_context('spameggs')
    assert ctx == {'spam': 1, 'eggs': 2}

def test_withall(tmpmod):
    """
    Tests what get's exported from a module with __all__
    """

    with tmpmod.mkdir("xontrib").join("spameggs.py").open('w') as x:
        x.write("""
__all__ = 'spam', '_foobar'
spam = 1
eggs = 2
_foobar = 3
""")

    ctx = xontrib_context('spameggs')
    assert ctx == {'spam': 1, '_foobar': 3}