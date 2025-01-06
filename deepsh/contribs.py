"""Tools for helping manage contributions."""

import contextlib
import importlib
import importlib.util
import json
import os
import sys
import typing as tp
from enum import IntEnum
from pathlib import Path

from deepsh.built_ins import XSH
from deepsh.cli_utils import Annotated, Arg, ArgParserAlias
from deepsh.completers.tools import RichCompletion
from deepsh.tools import print_color, print_exception

if tp.TYPE_CHECKING:
    from importlib.metadata import Distribution, EntryPoint


class ExitCode(IntEnum):
    OK = 0
    NOT_FOUND = 1
    INIT_FAILED = 2


class contribNotInstalled(Exception):
    """raised when the requested contrib is not found"""


class contrib(tp.NamedTuple):
    """Meta class that is used to describe a contrib"""

    module: str
    """path to the contrib module"""
    distribution: "tp.Optional[Distribution]" = None
    """short description about the contrib."""

    def get_description(self):
        if self.distribution:
            print(self, file=sys.stderr)
        if self.distribution and (
            summary := self.distribution.metadata.get("Summary", "")
        ):
            return summary
        return get_module_docstring(self.module)

    @property
    def url(self):
        if self.distribution:
            return self.distribution.metadata.get("Home-page", "")
        return ""

    @property
    def license(self):
        if self.distribution:
            return self.distribution.metadata.get("License", "")
        return ""

    @property
    def is_loaded(self):
        return self.module and self.module in sys.modules

    @property
    def is_auto_loaded(self):
        loaded = getattr(XSH.builtins, "autoloaded_contribs", None) or {}
        return self.module in set(loaded.values())


def get_module_docstring(module: str) -> str:
    """Find the module and return its docstring without actual import"""
    import ast

    spec = importlib.util.find_spec(module)
    if spec and spec.has_location and spec.origin:
        return ast.get_docstring(ast.parse(Path(spec.origin).read_text())) or ""
    return ""


def get_contribs() -> dict[str, contrib]:
    """Return contrib definitions lazily."""
    return dict(_get_installed_contribs())


def _patch_in_userdir():
    """
    Patch in user site packages directory.

    If deepsh is installed in non-writeable location, then contribs will end up
    there, so we make them accessible."""
    if not os.access(os.path.dirname(sys.executable), os.W_OK):
        from site import getusersitepackages

        if (user_site_packages := getusersitepackages()) not in set(sys.path):
            sys.path.append(user_site_packages)


def _get_installed_contribs(pkg_name="contrib"):
    """List all core packages + newly installed contribs"""
    _patch_in_userdir()
    spec = importlib.util.find_spec(pkg_name)

    def iter_paths():
        for loc in spec.submodule_search_locations:
            path = Path(loc)
            if path.exists():
                yield from path.iterdir()

    def iter_modules():
        # pkgutil is not finding `*.xsh` files
        for path in iter_paths():
            if path.suffix in {".py", ".xsh"}:
                yield path.stem

            elif path.is_dir():
                if (path / "__init__.py").exists():
                    yield path.name

    for name in iter_modules():
        module = f"contrib.{name}"
        yield name, contrib(module)

    for entry in _get_contrib_entrypoints():
        yield entry.name, contrib(entry.value, distribution=entry.dist)


def find_contrib(name, full_module=False):
    """Finds a contribution from its name."""
    _patch_in_userdir()

    # here the order is important. We try to run the correct cases first and then later trial cases
    # that will likely fail

    if name.startswith("."):
        return importlib.util.find_spec(name, package="contrib")

    if full_module:
        return importlib.util.find_spec(name)

    autoloaded = getattr(XSH.builtins, "autoloaded_contribs", None) or {}
    if name in autoloaded:
        return importlib.util.find_spec(autoloaded[name])

    with contextlib.suppress(ValueError):
        return importlib.util.find_spec("." + name, package="contrib")

    return importlib.util.find_spec(name)


def contrib_context(name, full_module=False):
    """Return a context dictionary for a contrib of a given name."""

    spec = find_contrib(name, full_module)
    if spec is None:
        return None
    module = importlib.import_module(spec.name)
    ctx = {}

    def _get__all__():
        pubnames = getattr(module, "__all__", None)
        if pubnames is None:
            for k in dir(module):
                if not k.startswith("_"):
                    yield k, getattr(module, k)
        else:
            for attr in pubnames:
                yield attr, getattr(module, attr)

    entrypoint = getattr(module, "_load_contrib_", None)
    if entrypoint is None:
        ctx.update(dict(_get__all__()))
    else:
        result = entrypoint(xsh=XSH)
        if result is not None:
            ctx.update(result)
    return ctx


def prompt_contrib_install(names: list[str]):
    """Returns a formatted string with name of contrib package to prompt user"""
    return (
        "The following contribs are enabled but not installed: \n"
        f"   {names}\n"
        "Please make sure that they are installed correctly by checking https://deepsh.github.io/awesome-contribs/\n"
    )


def update_context(name, ctx: dict, full_module=False):
    """Updates a context in place from a contrib."""
    modctx = contrib_context(name, full_module)
    if modctx is None:
        raise contribNotInstalled(f"contrib - {name} is not found.")
    else:
        ctx.update(modctx)
    return ctx


def _contrib_name_completions(loaded=False):
    for name, contrib in get_contribs().items():
        if contrib.is_loaded is loaded:
            yield RichCompletion(
                name, append_space=True, description=contrib.get_description()
            )


def contrib_names_completer(**_):
    yield from _contrib_name_completions(loaded=False)


def contrib_unload_completer(**_):
    yield from _contrib_name_completions(loaded=True)


def contribs_load(
    names: Annotated[
        tp.Sequence[str],
        Arg(nargs="+", completer=contrib_names_completer),
    ] = (),
    verbose=False,
    full_module=False,
    suppress_warnings=False,
):
    """Load contribs from a list of names

    Parameters
    ----------
    names
        names of contribs
    verbose : -v, --verbose
        verbose output
    full_module : -f, --full
        indicates that the names are fully qualified module paths and not inside ``contrib`` package
    suppress_warnings : -s, --suppress-warnings
        no warnings about missing contribs and return code 0
    """
    ctx = {} if XSH.ctx is None else XSH.ctx
    res = ExitCode.OK
    stdout = None
    stderr = None
    bad_imports = []
    for name in names:
        if verbose:
            print(f"loading contrib {name!r}")
        try:
            update_context(name, ctx=ctx, full_module=full_module)
        except contribNotInstalled:
            if not suppress_warnings:
                bad_imports.append(name)
        except Exception:
            res = ExitCode.INIT_FAILED
            print_exception(f"Failed to load contrib {name}.")
    if bad_imports:
        res = ExitCode.NOT_FOUND
        stderr = prompt_contrib_install(bad_imports)
    return stdout, stderr, res


def contribs_unload(
    names: Annotated[
        tp.Sequence[str],
        Arg(nargs="+", completer=contrib_unload_completer),
    ] = (),
    verbose=False,
):
    """Unload the given contribs

    Parameters
    ----------
    names
        name of contribs to unload

    Notes
    -----
    Proper cleanup can be implemented by the contrib. The default is equivalent to ``del sys.modules[module]``.
    """
    for name in names:
        if verbose:
            print(f"unloading contrib {name!r}")

        spec = find_contrib(name)
        try:
            if spec and spec.name in sys.modules:
                module = sys.modules[spec.name]
                unloader = getattr(module, "_unload_contrib_", None)
                if unloader is not None:
                    unloader(XSH)
                del sys.modules[spec.name]
        except Exception as ex:
            print_exception(f"Failed to unload contrib {name} ({ex})")


def contribs_reload(
    names: Annotated[
        tp.Sequence[str],
        Arg(nargs="+", completer=contrib_unload_completer),
    ] = (),
    verbose=False,
):
    """Reload the given contribs

    Parameters
    ----------
    names
        name of contribs to reload
    """
    for name in names:
        if verbose:
            print(f"reloading contrib {name!r}")
        contribs_unload([name])
        contribs_load([name])


def contrib_data():
    """Collects and returns the data about installed contribs."""
    data = {}
    for co_name, contrib in get_contribs().items():
        data[co_name] = {
            "name": co_name,
            "loaded": contrib.is_loaded,
            "auto": contrib.is_auto_loaded,
            "module": contrib.module,
        }

    return dict(sorted(data.items()))


def contribs_loaded():
    """Returns list of loaded contribs."""
    return [k for k, contrib in get_contribs().items() if contrib.is_loaded]


def contribs_list(to_json=False, _stdout=None):
    """List installed contribs and show whether they are loaded or not

    Parameters
    ----------
    to_json : -j, --json
        reports results as json
    """
    data = contrib_data()
    if to_json:
        s = json.dumps(data)
        return s
    else:
        nname = max([6] + [len(x) for x in data])
        s = ""
        for name, d in data.items():
            s += "{PURPLE}" + name + "{RESET}  " + " " * (nname - len(name))
            if d["loaded"]:
                s += "{GREEN}loaded{RESET}" + " " * 4
                if d["auto"]:
                    s += "  {GREEN}auto{RESET}"
                elif d["loaded"]:
                    s += "  {CYAN}manual{RESET}"
            else:
                s += "{RED}not-loaded{RESET}"
            s += "\n"
        print_color(s[:-1], file=_stdout)


def _get_contrib_entrypoints() -> "tp.Iterable[EntryPoint]":
    from importlib import metadata

    name = "deepsh.contribs"
    entries = metadata.entry_points()
    # for some reason, on CI (win py3.8) atleast, returns dict
    group = (
        entries.select(group=name)
        if hasattr(entries, "select")
        else entries.get(name, [])  # type: ignore
    )
    yield from group


def auto_load_contribs_from_entrypoints(
    blocked: "tp.Sequence[str]" = (), verbose=False
):
    """Load contrib modules exposed via setuptools's entrypoints"""

    if not hasattr(XSH.builtins, "autoloaded_contribs"):
        XSH.builtins.autoloaded_contribs = {}

    def get_loadable():
        for entry in _get_contrib_entrypoints():
            if entry.name not in blocked:
                XSH.builtins.autoloaded_contribs[entry.name] = entry.value
                yield entry.value

    modules = list(get_loadable())
    return contribs_load(modules, verbose=verbose, full_module=True)


class contribAlias(ArgParserAlias):
    """Manage deepsh extensions"""

    def build(self):
        parser = self.create_parser(prog="contrib")
        parser.add_command(contribs_load, prog="load")
        parser.add_command(contribs_unload, prog="unload")
        parser.add_command(contribs_reload, prog="reload")
        parser.add_command(contribs_list, prog="list", default=True)
        return parser


contribs_main = contribAlias(threadable=False)
