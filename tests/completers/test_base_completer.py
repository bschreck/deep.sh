import pytest

from deepsh.completers.base import complete_base
from deepsh.parsers.completion_context import CommandContext, CompletionContext
from deepsh.pytest.tools import ON_WINDOWS

CUR_DIR = (
    "." if ON_WINDOWS else "./"
)  # for some reason this is what happens in `complete_path`


@pytest.fixture(autouse=True)
def setup(xession, deepsh_execer, monkeypatch, mock_executables_in):
    xession.env["COMMANDS_CACHE_SAVE_INTERMEDIATE"] = False
    xession.env["COMPLETION_QUERY_LIMIT"] = 2000

    mock_executables_in(["cool"])


def test_empty_line(check_completer):
    completions = check_completer("")

    assert completions
    assert completions.issuperset({"cool", "abs"})
    for exp in ["cool", "abs"]:
        assert exp in completions


def test_empty_subexpr():
    completions = complete_base(
        CompletionContext(
            command=CommandContext((), 0, subcmd_opening="$("), python=None
        )
    )
    completions = set(map(str, completions))
    assert completions
    assert completions.issuperset({"cool"})
    assert "abs" not in completions
