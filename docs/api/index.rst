.. _api:

=================
Deepsh API
=================
For those of you who want the gritty details.


**Language:**

.. autosummary::
    :toctree: _autosummary/lang
    :template: api-summary-module.rst
    :recursive:

    deepsh.parsers.lexer
    deepsh.parser
    deepsh.parsers.ast
    deepsh.execer
    deepsh.imphooks


**Command Prompt:**

.. autosummary::
    :toctree: _autosummary/cmd
    :template: api-summary-module.rst
    :recursive:

    deepsh.built_ins
    deepsh.environ
    deepsh.aliases
    deepsh.dirstack
    deepsh.procs
    deepsh.lib.inspectors
    deepsh.history
    deepsh.completer
    deepsh.completers
    deepsh.prompt
    deepsh.shells
    deepsh.shells.base_shell
    deepsh.shells.readline_shell
    deepsh.shells.ptk_shell
    deepsh.lib.pretty
    deepsh.history.diff_history
    deepsh.coreutils


**Helpers:**

.. autosummary::
    :toctree: _autosummary/helpers
    :template: api-summary-module.rst
    :recursive:

    deepsh.events
    deepsh.lib
    deepsh.tools
    deepsh.platform
    deepsh.lazyjson
    deepsh.lazyasd
    deepsh.lib.openpy
    deepsh.foreign_shells
    deepsh.commands_cache
    deepsh.tracer
    deepsh.main
    deepsh.color_tools
    deepsh.pyghooks
    deepsh.shells.dumb_shell
    deepsh.wizard
    deepsh.config
    deepsh.contribs
    deepsh.codecache
    deepsh.contexts


**contribs:**

.. autosummary::
    :toctree: _autosummary/contribs
    :template: api-summary-module.rst
    :recursive:

    contrib
