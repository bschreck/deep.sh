from deepsh.cli_utils import ArgparseCompleter
from deepsh.parsers.completion_context import CommandContext


def deepsh_complete(command: CommandContext):
    """Completer for ``deepsh`` command using its ``argparser``"""

    from deepsh.main import parser

    completer = ArgparseCompleter(parser, command=command)
    return completer.complete(), False
