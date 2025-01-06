"""Testing for ``deepsh.shells.Shell``"""

import os

from deepsh.history.dummy import DummyHistory
from deepsh.history.json import JsonHistory
from deepsh.history.sqlite import SqliteHistory
from deepsh.shell import Shell


def test_shell_with_json_history(xession, deepsh_execer, tmpdir_factory):
    """
    Check that shell successfully load JSON history from file.
    """
    tempdir = str(tmpdir_factory.mktemp("history"))

    history_file = os.path.join(tempdir, "history.json")
    h = JsonHistory(filename=history_file)
    h.append(
        {
            "inp": "echo Hello world 1\n",
            "rtn": 0,
            "ts": [1615887820.7329783, 1615887820.7513437],
        }
    )
    h.append(
        {
            "inp": "echo Hello world 2\n",
            "rtn": 0,
            "ts": [1615887820.7329783, 1615887820.7513437],
        }
    )
    h.flush()

    xession.env.update(
        dict(
            DEEPSH_DATA_DIR=tempdir,
            DEEPSH_INTERACTIVE=True,
            DEEPSH_HISTORY_BACKEND="json",
            DEEPSH_HISTORY_FILE=history_file,
            # DEEPSH_DEBUG=1  # to show errors
        )
    )

    Shell(deepsh_execer, shell_type="none")

    assert len([i for i in xession.history.all_items()]) == 2


def test_shell_with_sqlite_history(xession, deepsh_execer, tmpdir_factory):
    """
    Check that shell successfully load SQLite history from file.
    """
    tempdir = str(tmpdir_factory.mktemp("history"))

    history_file = os.path.join(tempdir, "history.db")
    h = SqliteHistory(filename=history_file)
    h.append(
        {
            "inp": "echo Hello world 1\n",
            "rtn": 0,
            "ts": [1615887820.7329783, 1615887820.7513437],
        }
    )
    h.append(
        {
            "inp": "echo Hello world 2\n",
            "rtn": 0,
            "ts": [1615887820.7329783, 1615887820.7513437],
        }
    )
    h.flush()

    xession.env.update(
        dict(
            DEEPSH_DATA_DIR=tempdir,
            DEEPSH_INTERACTIVE=True,
            DEEPSH_HISTORY_BACKEND="sqlite",
            DEEPSH_HISTORY_FILE=history_file,
            # DEEPSH_DEBUG=1  # to show errors
        )
    )

    Shell(deepsh_execer, shell_type="none")

    assert len([i for i in xession.history.all_items()]) == 2


def test_shell_with_dummy_history_in_not_interactive(xession, deepsh_execer):
    """
    Check that shell use Dummy history in not interactive mode.
    """
    xession.env["DEEPSH_INTERACTIVE"] = False
    xession.history = None
    Shell(deepsh_execer, shell_type="none")
    assert isinstance(xession.history, DummyHistory)
