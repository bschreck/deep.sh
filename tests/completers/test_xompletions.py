import pytest


@pytest.mark.parametrize(
    "args, prefix, exp",
    [
        (
            "config",
            "-",
            {"-h", "--help"},
        ),
        (
            "config colors",
            "b",
            {"blue", "brown"},
        ),
    ],
)
def test_config(args, prefix, exp, xsh_with_aliases, monkeypatch, check_completer):
    from deepsh import config

    monkeypatch.setattr(config, "color_style_names", lambda: ["blue", "brown", "other"])
    assert check_completer(args, prefix=prefix) == exp


@pytest.mark.parametrize(
    "args, prefix, exp, exp_part",
    [
        (
            "contrib",
            "l",
            {"list", "load"},
            None,
        ),
        (
            "contrib load",
            "",
            None,
            {
                # the list may vary wrt the env. so testing only part of the coreutils.
                "coreutils",
            },
        ),
    ],
)
def test_contrib(args, prefix, exp, exp_part, xsh_with_aliases, check_completer):
    result = check_completer(args, prefix=prefix)
    if exp:
        assert result == exp
    if exp_part:
        assert result.issuperset(exp_part), f"{result} doesn't contain {exp_part} "


def test_module_matcher(tmp_path, xession):
    from deepsh.completers import commands

    for idx, ext in enumerate(commands.ModuleFinder.extensions):
        (tmp_path / f"a{idx}{ext}").write_text("def deepsh_complete(): pass")

    matcher = commands.ModuleFinder("completions", str(tmp_path))
    assert matcher.get_module("pip").deepsh_complete
    assert matcher.get_module("a0").deepsh_complete
    # todo: fix *.xsh import
    #  the import-hook returns None for some reason
    #  -- deepsh/imphooks.py:247
    # assert matcher.get_module("a1").deepsh_complete
