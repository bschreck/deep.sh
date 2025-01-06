"""DEPRECATED: Use `deepsh.lib.lazyjson` instead of `deepsh.lazyjson`."""

import warnings

warnings.warn(
    "Use `deepsh.lib.lazyjson` instead of `deepsh.lazyjson`.",
    DeprecationWarning,
    stacklevel=2,
)

from deepsh.lib.lazyjson import *  # noqa
