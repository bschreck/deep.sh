"""(A down payment on) Testing for ``deepsh.shells.base_shell.BaseShell`` and associated classes"""

import os

import pytest

from deepsh.shell import transform_command
from deepsh.shells.base_shell import BaseShell


def test_pwd_tracks_cwd(xession, deepsh_execer, tmpdir_factory, monkeypatch):
    asubdir = str(tmpdir_factory.mktemp("asubdir"))
    cur_wd = os.getcwd()
    xession.env.update(
        dict(PWD=cur_wd, DEEPSH_CACHE_SCRIPTS=False, DEEPSH_CACHE_EVERYTHING=False)
    )

    monkeypatch.setattr(deepsh_execer, "cacheall", False, raising=False)
    bc = BaseShell(deepsh_execer, None)

    assert os.getcwd() == cur_wd

    bc.default('os.chdir(r"' + asubdir + '")')

    assert os.path.abspath(os.getcwd()) == os.path.abspath(asubdir)
    assert os.path.abspath(os.getcwd()) == os.path.abspath(xession.env["PWD"])
    assert "OLDPWD" in xession.env
    assert os.path.abspath(cur_wd) == os.path.abspath(xession.env["OLDPWD"])


def test_transform(xession):
    @xession.builtins.events.on_transform_command
    def spam2egg(cmd, **_):
        if cmd == "spam":
            return "egg"
        else:
            return cmd

    assert transform_command("spam") == "egg"
    assert transform_command("egg") == "egg"
    assert transform_command("foo") == "foo"


@pytest.mark.parametrize(
    "cmd,exp_append_history",
    [
        ("", False),
        ("# a comment", False),
        ("print('yes')", True),
    ],
)
def test_default_append_history(cmd, exp_append_history, deepsh_session, monkeypatch):
    """Test that running an empty line or a comment does not append to history"""
    append_history_calls = []

    def mock_append_history(**info):
        append_history_calls.append(info)

    monkeypatch.setattr(
        deepsh_session.shell.shell, "_append_history", mock_append_history
    )
    deepsh_session.shell.default(cmd)
    if exp_append_history:
        assert len(append_history_calls) == 1
    else:
        assert len(append_history_calls) == 0
