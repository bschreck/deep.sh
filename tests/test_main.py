"""Tests the deepsh main function."""

import builtins
import gc
import os
import os.path
import sys
from contextlib import contextmanager
from pathlib import Path

import pytest

import deepsh.main
from deepsh.main import DeepshMode
from deepsh.pytest.tools import ON_WINDOWS, TEST_DIR, skip_if_on_windows


def Shell(*args, **kwargs):
    pass


@pytest.fixture
def shell(xession, monkeypatch):
    """Deepsh Shell Mock"""
    gc.collect()
    Shell.shell_type_aliases = {"rl": "readline"}
    monkeypatch.setattr(deepsh.main, "Shell", Shell)


@pytest.fixture(autouse=True)
def empty_deepshrc(monkeypatch):
    # Don't use the local machine's deepshrc
    empty_file_path = "NUL" if ON_WINDOWS else "/dev/null"
    monkeypatch.setitem(os.environ, "DEEPSHRC", empty_file_path)


def test_premain_no_arg(shell, monkeypatch, xession):
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    deepsh.main.premain([])
    assert xession.env.get("DEEPSH_LOGIN")


def test_premain_interactive(shell, xession):
    deepsh.main.premain(["-i"])
    assert xession.env.get("DEEPSH_INTERACTIVE")


def test_premain_login_command(shell, xession):
    deepsh.main.premain(["-l", "-c", 'echo "hi"'])
    assert xession.env.get("DEEPSH_LOGIN")


def test_premain_login(shell, xession):
    deepsh.main.premain(["-l"])
    assert xession.env.get("DEEPSH_LOGIN")


def test_premain_D(shell, xession):
    deepsh.main.premain(["-DTEST1=1616", "-DTEST2=LOL"])
    assert xession.env.get("TEST1") == "1616"
    assert xession.env.get("TEST2") == "LOL"


def test_premain_custom_rc(shell, tmpdir, monkeypatch, xession):
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setitem(os.environ, "DEEPSH_CACHE_SCRIPTS", "False")
    f = tmpdir.join("wakkawakka")
    f.write("print('hi')")
    args = deepsh.main.premain(["--rc", f.strpath])
    assert args.mode == DeepshMode.interactive
    assert f.strpath in xession.rc_files


@pytest.mark.skipif(
    ON_WINDOWS and sys.version_info[:3] == "3.8",
    reason="weird failure on py38+windows",
)
def test_rc_with_modules(shell, tmpdir, monkeypatch, capsys, xession):
    """Test that an RC file can load modules inside the same folder it is located in."""

    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setitem(os.environ, "DEEPSH_CACHE_SCRIPTS", "False")

    tmpdir.join("my_python_module.py").write("print('Hello,')")
    tmpdir.join("my_deepsh_module.xsh").write("print('World!')")
    rc = tmpdir.join("rc.xsh")
    rc.write("from my_python_module import *\nfrom my_deepsh_module import *")
    deepsh.main.premain(["--rc", rc.strpath])

    assert rc.strpath in xession.rc_files

    stdout, stderr = capsys.readouterr()
    assert "Hello,\nWorld!" in stdout
    assert len(stderr) == 0

    # Check that the temporary rc's folder is not left behind on the path
    assert tmpdir.strpath not in sys.path


def test_python_rc(shell, tmpdir, monkeypatch, capsys, xession, mocker):
    """Test that python based control files are executed using Python's parser"""

    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setitem(os.environ, "DEEPSH_CACHE_SCRIPTS", "False")

    # spy on deepsh's compile method
    spy = mocker.spy(xession.execer, "compile")

    rc = tmpdir.join("rc.py")
    rc.write("print('Hello World!')")
    deepsh.main.premain(["--rc", rc.strpath])

    assert rc.strpath in xession.rc_files

    stdout, stderr = capsys.readouterr()
    assert "Hello World!" in stdout
    assert len(stderr) == 0

    # Check that the temporary rc's folder is not left behind on the path
    assert tmpdir.strpath not in sys.path
    assert not spy.called


def test_rcdir(shell, tmpdir, monkeypatch, capsys):
    """
    Test that files are loaded from an rcdir, after a normal rc file,
    and in lecographic order.
    """

    rcdir = tmpdir.join("rc.d")
    rcdir.mkdir()
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setitem(os.environ, "DEEPSHRC_DIR", str(rcdir))
    monkeypatch.setitem(os.environ, "DEEPSHRC", str(tmpdir.join("rc.xsh")))
    monkeypatch.setitem(os.environ, "DEEPSH_CACHE_SCRIPTS", "False")

    rcdir.join("2.xsh").write("print('2.xsh')")
    rcdir.join("0.xsh").write("print('0.xsh')")
    rcdir.join("1.xsh").write("print('1.xsh')")
    tmpdir.join("rc.xsh").write("print('rc.xsh')")

    deepsh.main.premain([])
    stdout, stderr = capsys.readouterr()

    assert "rc.xsh\n0.xsh\n1.xsh\n2.xsh" in stdout
    assert len(stderr) == 0


def test_rcdir_cli(shell, tmpdir, xession, monkeypatch):
    """Test that --rc DIR works"""
    rcdir = tmpdir.join("rcdir")
    rcdir.mkdir()
    rc = rcdir.join("test.xsh")
    rc.write("print('test.xsh')")

    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    xargs = deepsh.main.premain(["--rc", rcdir.strpath])
    assert len(xargs.rc) == 1 and xargs.rc[0] == rcdir.strpath
    assert rc.strpath in xession.rc_files


def test_rcdir_empty(shell, tmpdir, monkeypatch, capsys):
    """Test that an empty DEEPSHRC_DIR is not an error"""

    rcdir = tmpdir.join("rc.d")
    rcdir.mkdir()
    rc = tmpdir.join("rc.xsh")
    rc.write_binary(b"")
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setitem(os.environ, "DEEPSHRC", str(rc))
    monkeypatch.setitem(os.environ, "DEEPSHRC_DIR", str(rcdir))

    deepsh.main.premain([])
    stdout, stderr = capsys.readouterr()
    assert len(stderr) == 0


# the parameterisation is a list of deepsh args, followed by the list
# of RC files (see function body) expected to be loaded in order
# note that a tty is not faked, so this will default to non-interactive
# (skipped on windows because DEEPSHRC="/path/to/f1.xsh:/path/to/f2.xsh"
# doesn't appear to work, while it does on other platforms)
@pytest.mark.skipif(ON_WINDOWS, reason="Issue with multi-file DEEPSHRC")
@pytest.mark.parametrize(
    ["args", "expected"],
    [
        # non-interactive, nothing loading
        [[], []],
        # interactive, normal DEEPSHRC and DEEPSHRC_DIR
        [["-i"], ["F0", "F1", "D0", "D1"]],
        # --no-rc wins over -i
        [["--no-rc", "-i"], []],
        # --no-rc wins over -i --rc
        [["--no-rc", "-i", "--rc", "<R0>"], []],
        # --rc does nothing in non-interactive mode
        [["--rc", "<R0>"], []],
        # but is respected in interactive
        [["-i", "--rc", "<R0>"], ["R0"]],
        # multiple invocations of --rc only use the last
        [["-i", "--rc", "<R0>", "--rc", "<R1>"], ["R1"]],
        # but multiple RC files can be specified after --rc
        [["-i", "--rc", "<R0>", "<R1>"], ["R0", "R1"]],
        # including the same file twice
        [["-i", "--rc", "<R0>", "<R0>"], ["R0", "R0"]],
        # scripts are non-interactive
        [["<SC>"], ["SC"]],
        # but -i will load the normal environment with a script
        [["-i", "<SC>"], ["F0", "F1", "D0", "D1", "SC"]],
        # no-rc has no effect on a script
        [["--no-rc", "<SC>"], ["SC"]],
        # but does prevent RC loading in -i mode
        [["--no-rc", "-i", "<SC>"], ["SC"]],
        # --rc doesn't work here because a script is non-interactive
        [["--rc", "<R0>", "--", "<SC>"], ["SC"]],
        # unless forced with -i
        [["-i", "--rc", "<R0>", "--", "<SC>"], ["R0", "SC"]],
        # --no-rc also wins here
        [["-i", "--rc", "<R0>", "--no-rc", "--", "<SC>"], ["SC"]],
        # single commands are non-interactive
        [["-c", "pass"], []],
        # but load RCs with -i
        [["-i", "-c", "pass"], ["F0", "F1", "D0", "D1"]],
        # --rc ignores without -i
        [["--rc", "<R0>", "-c", "pass"], []],
        # but used with -i
        [["-i", "--rc", "<R0>", "-c", "pass"], ["R0"]],
    ],
    ids=lambda ae: " ".join(ae),
)
def test_script_startup(shell, tmpdir, monkeypatch, capsys, args, expected):
    """
    Test the correct scripts are loaded, in the correct order, for
    different combinations of CLI arguments. See
    https://github.com/deepsh/deepsh/issues/4096

    This sets up a standard set of RC files which will be loaded,
    and tests whether they print their payloads at all, or in the right
    order, depending on the CLI arguments chosen.
    """
    rcdir = tmpdir.join("rc.d")
    rcdir.mkdir()
    # DEEPSHRC_DIR files, in order
    rcdir.join("d0.xsh").write("print('D0')")
    rcdir.join("d1.xsh").write("print('D1')")
    # DEEPSHRC files, in order
    f0 = tmpdir.join("f0.xsh")
    f0.write("print('F0')")
    f1 = tmpdir.join("f1.xsh")
    f1.write("print('F1')")
    # RC files which can be explicitly loaded with --rc
    r0 = tmpdir.join("r0.xsh")
    r0.write("print('R0')")
    r1 = tmpdir.join("r1.xsh")
    r1.write("print('R1')")
    # a (non-RC) script which can be loaded
    sc = tmpdir.join("sc.xsh")
    sc.write("print('SC')")

    monkeypatch.setitem(os.environ, "DEEPSHRC", f"{f0}:{f1}")
    monkeypatch.setitem(os.environ, "DEEPSHRC_DIR", str(rcdir))

    # replace <RC> with the path to rc.xsh and <SC> with sc.xsh
    args = [
        a.replace("<R0>", str(r0)).replace("<R1>", str(r1)).replace("<SC>", str(sc))
        for a in args
    ]

    # since we only test deepsh.premain here, a script file (SC)
    # won't actually get run here, so won't appear in the stdout,
    # so don't check for it (but check for a .file in the parsed args)
    check_for_script = "SC" in expected
    expected = [e for e in expected if e != "SC"]

    xargs = deepsh.main.premain(args)
    stdout, stderr = capsys.readouterr()
    assert "\n".join(expected) in stdout
    if check_for_script:
        assert xargs.file is not None


def test_rcdir_ignored_with_rc(shell, tmpdir, monkeypatch, capsys, xession):
    """Test that --rc suppresses loading DEEPSHRC_DIRs"""

    rcdir = tmpdir.join("rc.d")
    rcdir.mkdir()
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setitem(os.environ, "DEEPSHRC_DIR", str(rcdir))
    rcdir.join("rcd.xsh").write("print('RCDIR')")
    tmpdir.join("rc.xsh").write("print('RCFILE')")

    deepsh.main.premain(["--rc", str(tmpdir.join("rc.xsh"))])
    stdout, stderr = capsys.readouterr()
    assert "RCDIR" not in stdout
    assert "RCFILE" in stdout
    assert str(rcdir.join("rcd.xsh")) not in xession.rc_files


@pytest.mark.skipif(ON_WINDOWS, reason="See https://github.com/deepsh/deepsh/issues/3936")
def test_rc_with_modified_path(shell, tmpdir, monkeypatch, capsys, xession):
    """Test that an RC file can edit the sys.path variable without losing those values."""

    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setitem(os.environ, "DEEPSH_CACHE_SCRIPTS", "False")

    rc = tmpdir.join("rc.xsh")
    rc.write(f"import sys\nsys.path.append('{tmpdir.strpath}')\nprint('Hello, World!')")
    deepsh.main.premain(["--rc", rc.strpath])

    assert rc.strpath in xession.rc_files

    stdout, stderr = capsys.readouterr()
    assert "Hello, World!" in stdout
    assert len(stderr) == 0

    # Check that the path that was explicitly added is not accidentally deleted
    assert tmpdir.strpath in sys.path


def test_rc_with_failing_module(shell, tmpdir, monkeypatch, capsys, xession):
    """Test that an RC file which imports a module that throws an exception ."""

    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setitem(os.environ, "DEEPSH_CACHE_SCRIPTS", "False")

    tmpdir.join("my_failing_module.py").write("raise RuntimeError('Unexpected error')")
    rc = tmpdir.join("rc.xsh")
    rc.write("from my_failing_module import *")
    deepsh.main.premain(["--rc", rc.strpath])

    assert rc.strpath not in xession.rc_files

    stdout, stderr = capsys.readouterr()
    assert len(stdout) == 0
    assert "Unexpected error" in stderr

    # Check that the temporary rc's folder is not left behind on the path
    assert tmpdir.strpath not in sys.path


def test_no_rc_with_script(shell, tmpdir):
    args = deepsh.main.premain(["tests/sample.xsh"])
    assert not (args.mode == DeepshMode.interactive)


def test_force_interactive_rc_with_script(shell, tmpdir, xession):
    deepsh.main.premain(["-i", "tests/sample.xsh"])
    assert xession.env.get("DEEPSH_INTERACTIVE")


def test_force_interactive_custom_rc_with_script(shell, tmpdir, monkeypatch, xession):
    """Calling a custom RC file on a script-call with the interactive flag
    should run interactively
    """
    monkeypatch.setitem(os.environ, "DEEPSH_CACHE_SCRIPTS", "False")
    f = tmpdir.join("wakkawakka")
    f.write("print('hi')")
    args = deepsh.main.premain(
        ["-i", "--rc", f.strpath, str(Path(__file__).parent / "sample.xsh")]
    )
    assert args.mode == DeepshMode.interactive
    assert f.strpath in xession.rc_files


def test_force_interactive_custom_rc_with_script_and_no_rc(
    shell, tmpdir, monkeypatch, xession
):
    monkeypatch.setitem(os.environ, "DEEPSH_CACHE_SCRIPTS", "False")
    f = tmpdir.join("wakkawakka")
    f.write("print('hi')")
    args = deepsh.main.premain(
        ["-i", "--no-rc", "--rc", f.strpath, str(Path(__file__).parent / "sample.xsh")]
    )
    assert args.mode == DeepshMode.interactive
    assert len(xession.rc_files) == 0


def test_custom_rc_with_script(shell, tmpdir, xession):
    """Calling a custom RC file on a script-call without the interactive flag
    should not run interactively
    """
    f = tmpdir.join("wakkawakka")
    f.write("print('hi')")
    args = deepsh.main.premain(
        ["--rc", f.strpath, str(Path(__file__).parent / "sample.xsh")]
    )
    assert not (args.mode == DeepshMode.interactive)
    assert f.strpath in xession.rc_files


def test_custom_rc_with_script_and_no_rc(shell, tmpdir, xession):
    """Calling a custom RC file on a script-call without the interactive flag and no-rc
    should not run interactively and should not have any rc_files
    """
    f = tmpdir.join("wakkawakka")
    f.write("print('hi')")
    args = deepsh.main.premain(
        ["--no-rc", "--rc", f.strpath, str(Path(__file__).parent / "sample.xsh")]
    )
    assert not (args.mode == DeepshMode.interactive)
    assert len(xession.rc_files) == 0


def test_premain_no_rc(shell, tmpdir, xession):
    deepsh.main.premain(["--no-rc"])
    assert len(xession.rc_files) == 0


def test_premain_no_rc_interactive(shell, tmpdir, xession):
    deepsh.main.premain(["--no-rc", "-i"])
    assert len(xession.rc_files) == 0


@pytest.mark.parametrize(
    "arg", ["", "-i", "-vERSION", "-hAALP", "TTTT", "-TT", "--TTT"]
)
def test_premain_with_file_argument(arg, shell, xession):
    deepsh.main.premain(["tests/sample.xsh", arg])
    assert not (xession.env.get("DEEPSH_INTERACTIVE"))


def test_premain_interactive__with_file_argument(shell, xession):
    deepsh.main.premain(["-i", "tests/sample.xsh"])
    assert xession.env.get("DEEPSH_INTERACTIVE")


@pytest.mark.parametrize("case", ["----", "--hep", "-TT", "--TTTT"])
def test_premain_invalid_arguments(shell, case, capsys):
    with pytest.raises(SystemExit):
        deepsh.main.premain([case])
    assert "unrecognized argument" in capsys.readouterr()[1]


def test_premain_timings_arg(shell):
    deepsh.main.premain(["--timings"])


@skip_if_on_windows
@pytest.mark.parametrize(
    ("env_shell", "rc_shells", "exp_shell"),
    [
        ("", [], ""),
        ("/argle/bash", [], "/argle/bash"),
        ("/bin/deepsh", [], ""),
        (
            "/argle/bash",
            ["/argle/deepsh", "/argle/dash", "/argle/sh", "/argle/bargle"],
            "/argle/bash",
        ),
        (
            "",
            ["/argle/deepsh", "/argle/dash", "/argle/sh", "/argle/bargle"],
            "/argle/dash",
        ),
        ("", ["/argle/deepsh", "/argle/screen", "/argle/sh"], "/argle/sh"),
        ("", ["/argle/deepsh", "/argle/screen"], ""),
    ],
)
@skip_if_on_windows
def test_deepsh_failback(
    env_shell,
    rc_shells,
    exp_shell,
    shell,
    xession,
    monkeypatch,
    monkeypatch_stderr,
):
    failback_checker = []

    def mocked_main(*args):
        raise Exception("A fake failure")

    monkeypatch.setattr(deepsh.main, "main_deepsh", mocked_main)

    def mocked_execlp(f, *args):
        failback_checker.append(f)
        failback_checker.append(args[0])

    monkeypatch.setattr(os, "execlp", mocked_execlp)
    monkeypatch.setattr(os.path, "exists", lambda x: True)
    monkeypatch.setattr(sys, "argv", ["/bin/deepsh", "-i"])  # has to look like real path

    @contextmanager
    def mocked_open(*args):
        yield rc_shells

    monkeypatch.setattr(builtins, "open", mocked_open)

    monkeypatch.setenv("SHELL", env_shell)

    try:
        deepsh.main.main()  # if main doesn't raise, it did try to invoke a shell
        assert failback_checker[0] == exp_shell
        assert failback_checker[1] == failback_checker[0]
    except Exception as e:
        if len(e.args) and "A fake failure" in str(
            e.args[0]
        ):  # if it did raise expected exception
            assert len(failback_checker) == 0  # then it didn't invoke a shell
        else:
            raise e  # it raised something other than the test exception,


def test_deepsh_failback_single(shell, monkeypatch, monkeypatch_stderr):
    class FakeFailureError(Exception):
        pass

    def mocked_main(*args):
        raise FakeFailureError()

    monkeypatch.setattr(deepsh.main, "main_deepsh", mocked_main)
    monkeypatch.setattr(sys, "argv", ["deepsh", "-c", "echo", "foo"])

    with pytest.raises(FakeFailureError):
        deepsh.main.main()


def test_deepsh_failback_script_from_file(shell, monkeypatch, monkeypatch_stderr):
    checker = []

    def mocked_execlp(f, *args):
        checker.append(f)

    monkeypatch.setattr(os, "execlp", mocked_execlp)

    script = os.path.join(TEST_DIR, "scripts", "raise.xsh")
    monkeypatch.setattr(sys, "argv", ["deepsh", script])

    # changed in #4662: User-Code exceptions are now caught in main and handled there
    # => we expect that no exception is thrown

    assert len(checker) == 0


def test_deepsh_no_file_returncode(shell, monkeypatch, monkeypatch_stderr):
    monkeypatch.setattr(sys, "argv", ["deepsh", "foobazbarzzznotafileatall.xsh"])
    with pytest.raises(SystemExit):
        deepsh.main.main()


def test_auto_loading_contribs(xession, shell, mocker):
    from importlib.metadata import EntryPoint

    group = "deepsh.contribs"

    mocker.patch(
        "importlib.metadata.entry_points",
        autospec=True,
        return_value={
            group: [EntryPoint(name="test", group=group, value="test.module")]
        },
    )
    contribs_load = mocker.patch("deepsh.contribs.contribs_load")
    deepsh.main.premain([])
    assert xession.builtins.autoloaded_contribs == {"test": "test.module"}
    contribs_load.assert_called()
