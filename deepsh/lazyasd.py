"""DEPRECATED: Use `deepsh.lib.lazyasd` instead of `deepsh.lazyasd`."""

import warnings

warnings.warn(
    "Use `deepsh.lib.lazyasd` instead of `deepsh.lazyasd`.",
    DeprecationWarning,
    stacklevel=2,
)

from deepsh.lib.lazyasd import *  # noqa
