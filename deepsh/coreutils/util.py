"""Assorted utilities for deepsh core utils."""


def arg_handler(args, out, short, key, val, long=None):
    """A simple argument handler for coreutils."""
    if short in args:
        args.remove(short)
        if isinstance(key, (list, tuple)):
            for k in key:
                out[k] = val
        else:
            out[key] = val
    if long is not None and long in args:
        args.remove(long)
        if isinstance(key, (list, tuple)):
            for k in key:
                out[k] = val
        else:
            out[key] = val


def run_alias(name: str, args=None):
    import sys

    from deepsh.built_ins import subproc_uncaptured
    from deepsh.main import setup
    from deepsh.contribs import contribs_load

    setup()

    contribs_load(["coreutils"])
    args = sys.argv[1:] if args is None else args

    subproc_uncaptured([name] + args)
