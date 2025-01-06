"""Completers for pip."""

from deepsh.completers.tools import comp_based_completer
from deepsh.parsers.completion_context import CommandContext


def deepsh_complete(ctx: CommandContext):
    """Completes python's package manager pip."""

    return comp_based_completer(ctx, PIP_AUTO_COMPLETE="1")
