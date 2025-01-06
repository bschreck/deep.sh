"""DEPRECATED: Use `deepsh.lib.lazyasd` instead of `deepsh.lazyasd`."""

import warnings

warnings.warn(
    "Use `deepsh.api.os` instead of `deepsh.lib.os`.", DeprecationWarning, stacklevel=2
)

from deepsh.api.os import *  # noqa
