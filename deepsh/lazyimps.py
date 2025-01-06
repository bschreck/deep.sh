"""DEPRECATED: Use `deepsh.lib.lazyasd` instead of `deepsh.lazyimps`."""

import warnings

warnings.warn(
    "Use `deepsh.lib.lazyimps` instead of `deepsh.lazyimps`.",
    DeprecationWarning,
    stacklevel=2,
)

from deepsh.lib.lazyimps import *  # noqa
