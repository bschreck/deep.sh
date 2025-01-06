"""
Tests for command pipelines.
"""

import os

import pytest

from deepsh.platform import ON_WINDOWS
from deepsh.procs.pipelines import CommandPipeline
from deepsh.pytest.tools import (
    VER_MAJOR_MINOR,
    skip_if_on_unix,
    skip_if_on_windows,
)

# TODO: track down which pipeline + spec test is hanging CI
# Skip entire test file for Linux on Python 3.12
pytestmark = pytest.mark.skipif(
    not ON_WINDOWS and VER_MAJOR_MINOR == (3, 12),
    reason="Backgrounded test is hanging on CI on 3.12 only",
    allow_module_level=True,
)


@pytest.fixture(autouse=True)
def patched_events(monkeypatch, deepsh_events, deepsh_session):
    from deepsh.procs.jobs import get_tasks

    get_tasks().clear()
    # needed for ci tests
    monkeypatch.setitem(
        deepsh_session.env, "RAISE_SUBPROC_ERROR", False
    )  # for the failing `grep` commands
    monkeypatch.setitem(
        deepsh_session.env, "DEEPSH_CAPTURE_ALWAYS", True
    )  # capture output of ![]
    if ON_WINDOWS:
        monkeypatch.setattr(
            deepsh_session.commands_cache,
            "aliases",
            {
                "echo": "cmd /c echo".split(),
                "grep": "cmd /c findstr".split(),
            },
            raising=False,
        )


@pytest.mark.parametrize(
    "cmdline, stdout, stderr, raw_stdout",
    (
        ("!(echo hi)", "hi", "", "hi\n"),
        ("!(echo hi o>e)", "", "hi\n", ""),
        pytest.param(
            "![echo hi]",
            "hi",
            "",
            "hi\n",
            marks=pytest.mark.xfail(
                ON_WINDOWS,
                reason="ConsoleParallelReader doesn't work without a real console",
            ),
        ),
        pytest.param(
            "![echo hi o>e]",
            "",
            "hi\n",
            "",
            marks=pytest.mark.xfail(
                ON_WINDOWS, reason="stderr isn't captured in ![] on windows"
            ),
        ),
        pytest.param(
            r"!(echo 'hi\nho')", "hi\nho\n", "", "hi\nho\n", marks=skip_if_on_windows
        ),  # won't work with cmd
        # for some reason cmd's echo adds an extra space:
        pytest.param(
            r"!(cmd /c 'echo hi && echo ho')",
            "hi \nho\n",
            "",
            "hi \nho\n",
            marks=skip_if_on_unix,
        ),
        ("!(echo hi | grep h)", "hi", "", "hi\n"),
        ("!(echo hi | grep x)", "", "", ""),
    ),
)
@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_command_pipeline_capture(cmdline, stdout, stderr, raw_stdout, deepsh_execer):
    pipeline: CommandPipeline = deepsh_execer.eval(cmdline)
    assert pipeline.out == stdout
    assert pipeline.err == (stderr or None)
    assert pipeline.raw_out == raw_stdout.replace("\n", os.linesep).encode()
    assert pipeline.raw_err == stderr.replace("\n", os.linesep).encode()


@pytest.mark.parametrize(
    "cmdline, output",
    (
        ("echo hi", "hi"),
        ("echo hi | grep h", "hi"),
        ("echo hi | grep x", ""),
        pytest.param("echo -n hi", "hi", marks=skip_if_on_windows),
    ),
)
def test_simple_capture(cmdline, output, deepsh_execer):
    assert deepsh_execer.eval(f"$({cmdline})") == output


def test_raw_substitution(deepsh_execer):
    assert deepsh_execer.eval("$(echo @(b'bytes!'))") == "bytes!"


@pytest.mark.parametrize(
    "cmdline, result",
    (
        ("bool(!(echo 1))", True),
        ("bool(!(nocommand))", False),
        ("int(!(echo 1))", 0),
        ("int(!(nocommand))", 1),
        ("hash(!(echo 1))", 0),
        ("hash(!(nocommand))", 1),
        ("str(!(echo 1))", "1"),
        ("str(!(nocommand))", ""),
        ("!(echo 1) == 0", True),
        ("!(nocommand) == 1", True),
        pytest.param("!(echo -n str) == 'str'", True, marks=skip_if_on_windows),
        ("!(nocommand) == ''", True),
    ),
)
def test_casting(cmdline, result, deepsh_execer):
    assert deepsh_execer.eval(f"{cmdline}") == result


@skip_if_on_windows
@skip_if_on_unix
def test_background_pgid(deepsh_session, monkeypatch):
    monkeypatch.setitem(deepsh_session.env, "DEEPSH_INTERACTIVE", True)
    pipeline = deepsh_session.execer.eval("![echo hi &]")
    assert pipeline.term_pgid is not None
