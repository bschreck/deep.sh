import platform

import pytest


@pytest.fixture
def uname(xession, load_contrib):
    load_contrib("coreutils")
    return xession.aliases["uname"]


def test_uname_without_args(uname):
    out = uname(["-a"])

    assert out.startswith(platform.uname().system)
