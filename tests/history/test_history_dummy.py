"""Tests the dummy history backend."""

import pytest

from deepsh.history.dummy import DummyHistory
from deepsh.history.main import construct_history


@pytest.mark.parametrize("backend", ["dummy", DummyHistory, DummyHistory()])
def test_construct_history_str(xession, backend):
    xession.env["DEEPSH_HISTORY_BACKEND"] = backend
    assert isinstance(construct_history(), DummyHistory)


def test_ignore_regex_invalid(xession, capsys):
    xession.env["DEEPSH_HISTORY_BACKEND"] = "dummy"
    xession.env["DEEPSH_HISTORY_IGNORE_REGEX"] = "**"
    history = construct_history()
    captured = capsys.readouterr()
    assert (
        "DEEPSH_HISTORY_IGNORE_REGEX is not a valid regular expression and will be ignored"
        in captured.err
    )
    assert not history.is_ignored({"inp": "history"})


def test_is_ignore(xession):
    xession.env["DEEPSH_HISTORY_BACKEND"] = "dummy"
    xession.env["DEEPSH_HISTORY_IGNORE_REGEX"] = "(ls|cat)"
    history = construct_history()
    assert history.is_ignored({"inp": "cat foo.txt"})
    assert not history.is_ignored({"inp": "history"})
    assert history.is_ignored({"inp": "ls bar"})


def test_is_ignore_no_regex(xession):
    xession.env["DEEPSH_HISTORY_BACKEND"] = "dummy"
    history = construct_history()
    assert not history.is_ignored({"inp": "cat foo.txt"})
    assert not history.is_ignored({"inp": "history"})
    assert not history.is_ignored({"inp": "ls bar"})
