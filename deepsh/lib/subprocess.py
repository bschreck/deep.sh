"""DEPRECATED: Use `deepsh.lib.lazyasd` instead of `deepsh.lazyasd`."""

import warnings

warnings.warn(
    "Use `deepsh.api.subprocess` instead of `deepsh.lib.subprocess`.",
    DeprecationWarning,
    stacklevel=2,
)

from deepsh.api.subprocess import *  # noqa
