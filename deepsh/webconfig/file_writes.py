"""functions to update rc files"""

import os
import re
import typing as tp

from deepsh.environ import get_home_deepshrc_path


def write_value(value: str, _) -> str:
    return f"{value!r}"


def append_to_list(value: list[str], existing: str) -> str:
    vals = set(existing.split(" ")) if existing else set()
    vals.update(value)
    return " ".join(vals)


RENDERERS: dict[str, tuple[str, tp.Callable[[tp.Any, str], str]]] = {
    "$PROMPT = ": ("prompt", write_value),
    "$DEEPSH_COLOR_STYLE = ": ("color", write_value),
    "contrib load ": ("contribs", append_to_list),
}


def config_to_deepsh(
    config: dict,
    prefix="# DEEPSH WEBCONFIG START",
    current_lines: "tp.Iterable[str]" = (),
    suffix="# DEEPSH WEBCONFIG END",
):
    """Turns config dict into deepsh code (str)."""
    yield prefix
    renderers = set(RENDERERS)
    for existing in current_lines:
        if start := next(filter(lambda x: existing.startswith(x), renderers), None):
            renderers.remove(start)
            key, func = RENDERERS[start]
            if value := config.get(key):
                yield start + func(value, existing.strip(start))
            else:
                yield existing
        else:
            yield existing

    for start in renderers:
        key, func = RENDERERS[start]
        if value := config.get(key):
            yield start + func(value, "")

    yield suffix


RC_FILE = get_home_deepshrc_path()


def insert_into_deepshrc(
    config: dict,
    deepshrc=None,
    prefix="# DEEPSH WEBCONFIG START",
    suffix="# DEEPSH WEBCONFIG END",
):
    """Places a config dict into the deepshrc."""
    if deepshrc is None:
        deepshrc = RC_FILE
    current_lines = []
    # get current contents
    fname = os.path.expanduser(deepshrc)
    if os.path.isfile(fname):
        with open(fname) as f:
            s = f.read()
        before, _, s = s.partition(prefix)
        current, _, after = s.partition(suffix)
        current_lines = current.strip().splitlines(keepends=False)
    else:
        before = after = ""
        dname = os.path.dirname(fname)
        if dname:
            os.makedirs(dname, exist_ok=True)
    # compute new values
    lines = config_to_deepsh(
        config,
        prefix=prefix,
        current_lines=current_lines,
        suffix=suffix,
    )
    # write out the file
    with open(fname, "w", encoding="utf-8") as f:
        f.write(before + re.sub(r"\\r", "", "\n".join(lines)) + after)
    return fname
