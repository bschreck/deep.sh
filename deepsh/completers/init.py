"""Constructor for deepsh completer objects."""

import collections

from deepsh.completers._aliases import complete_aliases
from deepsh.completers.base import complete_base
from deepsh.completers.bash import complete_from_bash
from deepsh.completers.commands import (
    complete_end_proc_keywords,
    complete_end_proc_tokens,
    complete_skipper,
    complete_completions,
)
from deepsh.completers.environment import complete_environment_vars
from deepsh.completers.imports import complete_import
from deepsh.completers.man import complete_from_man
from deepsh.completers.path import complete_path
from deepsh.completers.python import complete_python


def default_completers(cmd_cache):
    """Creates a copy of the default completers."""
    defaults = [
        # non-exclusive completers:
        ("end_proc_tokens", complete_end_proc_tokens),
        ("end_proc_keywords", complete_end_proc_keywords),
        ("environment_vars", complete_environment_vars),
        # exclusive completers:
        ("base", complete_base),
        ("skip", complete_skipper),
        ("alias", complete_aliases),
        ("completer", complete_completions),
        ("import", complete_import),
    ]

    for cmd, func in [
        ("bash", complete_from_bash),
        ("man", complete_from_man),
    ]:
        if cmd in cmd_cache:
            defaults.append((cmd, func))

    defaults.extend(
        [
            ("python", complete_python),
            ("path", complete_path),
        ]
    )
    return collections.OrderedDict(defaults)
