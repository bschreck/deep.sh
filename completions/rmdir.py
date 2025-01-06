from deepsh.completers.path import complete_dir
from deepsh.parsers.completion_context import CommandContext


def deepsh_complete(ctx: CommandContext):
    """
    Completion for "rmdir", includes only valid directory names.
    """
    # if starts with the given prefix then it will get completions from man page
    if not ctx.prefix.startswith("-") and ctx.arg_index > 0:
        comps, lprefix = complete_dir(ctx)
        if not comps:
            raise StopIteration  # no further file completions
        return comps, lprefix
