from deepsh.completers.path import complete_dir
from deepsh.parsers.completion_context import CommandContext


def deepsh_complete(command: CommandContext):
    """
    Completion for "cd", includes only valid directory names.
    """
    results, lprefix = complete_dir(command)
    if len(results) == 0:
        raise StopIteration
    return results, lprefix
