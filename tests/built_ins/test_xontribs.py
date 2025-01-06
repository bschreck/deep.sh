"""contrib tests, such as they are"""

import sys

import pytest

from deepsh.contribs import (
    contrib_context,
    contribs_load,
    contribs_loaded,
    contribs_main,
    contribs_reload,
    contribs_unload,
)


@pytest.fixture
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

    with tmpmod.mkdir("contrib").join("spameggs.py").open("w") as x:
        x.write(
            """
spam = 1
eggs = 2
_foobar = 3
"""
        )

    ctx = contrib_context("spameggs")
    assert ctx == {"spam": 1, "eggs": 2}


def test_withall(tmpmod):
    """
    Tests what get's exported from a module with __all__
    """

    with tmpmod.mkdir("contrib").join("spameggs.py").open("w") as x:
        x.write(
            """
__all__ = 'spam', '_foobar'
spam = 1
eggs = 2
_foobar = 3
"""
        )

    ctx = contrib_context("spameggs")
    assert ctx == {"spam": 1, "_foobar": 3}


def test_xshcontrib(tmpmod):
    """
    Test that .xsh contribs are loadable
    """
    with tmpmod.mkdir("contrib").join("script.xsh").open("w") as x:
        x.write(
            """
hello = 'world'
"""
        )

    ctx = contrib_context("script")
    assert ctx == {"hello": "world"}


def test_contrib_load(tmpmod):
    """
    Test that .xsh contribs are loadable
    """
    with tmpmod.mkdir("contrib").join("script.xsh").open("w") as x:
        x.write(
            """
hello = 'world'
"""
        )

    contribs_load(["script"])
    assert "script" in contribs_loaded()


def test_contrib_unload(tmpmod, xession):
    with tmpmod.mkdir("contrib").join("script.py").open("w") as x:
        x.write(
            """
hello = 'world'

def _unload_contrib_(xsh): del xsh.ctx['hello']
"""
        )

    contribs_load(["script"])
    assert "script" in contribs_loaded()
    assert "hello" in xession.ctx
    contribs_unload(["script"])
    assert "script" not in contribs_loaded()
    assert "hello" not in xession.ctx


def test_contrib_reload(tmpmod, xession):
    with tmpmod.mkdir("contrib").join("script.py").open("w") as x:
        x.write(
            """
hello = 'world'

def _unload_contrib_(xsh): del xsh.ctx['hello']
"""
        )

    contribs_load(["script"])
    assert "script" in contribs_loaded()
    assert xession.ctx["hello"] == "world"

    with tmpmod.join("contrib").join("script.py").open("w") as x:
        x.write(
            """
hello = 'world1'

def _unload_contrib_(xsh): del xsh.ctx['hello']
"""
        )
    contribs_reload(["script"])
    assert "script" in contribs_loaded()
    assert xession.ctx["hello"] == "world1"


def test_contrib_load_dashed(tmpmod):
    """
    Test that .xsh contribs are loadable
    """
    with tmpmod.mkdir("contrib").join("scri-pt.xsh").open("w") as x:
        x.write(
            """
hello = 'world'
"""
        )

    contribs_load(["scri-pt"])
    assert "scri-pt" in contribs_loaded()


def test_contrib_list(xession, capsys):
    contribs_main(["list"])
    out, err = capsys.readouterr()
    assert "coreutils" in out
