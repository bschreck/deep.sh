.. _tutorial_xontrib:

************************************
Tutorial: Extensions (Xontribs)
************************************
Take a deep breath and prepare for some serious Show & Tell; it's time to
learn about deepsh extensions!

Deepsh comes with some default set of extensions. These can be viewed :py:mod:`here <xontrib>`.

Also checkout the list of `Awesome Contributions <https://deepsh.github.io/awesome-xontribs/>`_
from the community.

Overview
========
Xontributions, or ``xontribs``, are a set of tools and conventions for
extending the functionality of deepsh beyond what is provided by default. This
allows 3rd party developers and users to improve their deepsh experience without
having to go through the deepsh development and release cycle.

Many tools and libraries have extension capabilities. Here are some that we
took inspiration from for deepsh:

* `Sphinx <http://sphinx-doc.org/>`_: Extensions are just Python modules,
  bundles some extensions with the main package, interface is a list of
  string names.
* `IPython <https://ipython.readthedocs.io/en/stable/config/extensions/index.html>`_: Extensions are just Python modules
  with some special functions to load/unload.
* `Oh My Zsh <http://ohmyz.sh/>`_: Centralized registry, autoloading, and
  for a shell.
* `ESLint <http://eslint.org/>`_: Ability to use language package manager
  to install/remove extensions.

Structure
================
Xontribs are modules with some special functions written
in either deepsh (``*.xsh``) or Python (``*.py``).

Here is a template:

.. code-block:: python

    from deepsh.built_ins import DeepshSession

    def _load_xontrib_(xsh: DeepshSession, **kwargs) -> dict:
        """
        this function will be called when loading/reloading the xontrib.

        Args:
            xsh: the current deepsh session instance, serves as the interface to manipulate the session.
                 This allows you to register new aliases, history backends, event listeners ...
            **kwargs: it is empty as of now. Kept for future proofing.
        Returns:
            dict: this will get loaded into the current execution context
        """

    def _unload_xontrib_(xsh: DeepshSession, **kwargs) -> dict:
        """If you want your extension to be unloadable, put that logic here"""

This _load_xontrib_() function is called after your extension is imported,
and the currently active :py:class:`deepsh.built_ins.DeepshSession` instance is passed as the argument.

.. note::

    Xontribs without ``_load_xontrib_`` are still supported.
    But when such xontrib is loaded, variables listed
    in ``__all__`` are placed in the current
    execution context if defined.

Normally, these are stored and found in an
`implicit namespace package <https://www.python.org/dev/peps/pep-0420/>`_
called ``xontrib``. However, xontribs may be placed in any package or directory
that is on the ``$PYTHONPATH``.

If a module is in the ``xontrib`` namespace package, it can be referred to just
by its module name. If a module is in any other package, then it must be
referred to by its full package path, separated by ``.`` like you would in an
import statement.  Of course, a module in ``xontrib`` may be referred to
with the full ``xontrib.myext``. But just calling it ``myext`` is a lot shorter
and one of the main advantages of placing an extension in the ``xontrib``
namespace package.

Here is a sample file system layout and what the xontrib names would be::

    |- xontrib/
       |- javert.xsh     # "javert", because in xontrib
       |- your.py        # "your",
       |- eyes/
          |- __init__.py
          |- scream.xsh  # "eyes.scream", because eyes is in xontrib
    |- mypkg/
       |- __init__.py    # a regular package with an init file
       |- other.py       # not a xontrib
       |- show.py        # "mypkg.show", full module name
       |- tell.xsh       # "mypkg.tell", full module name
       |- subpkg/
          |- __init__.py
          |- done.py     # "mypkg.subpkg.done", full module name


You can also use the `xontrib template <https://github.com/deepsh/xontrib-cookiecutter>`_ to easily
create the layout for your xontrib package.


Loading Xontribs
================
Xontribs may be loaded in a few different ways: from the `deepshrc <deepshrc.rst>`_ file
(e.g. ``~/.deepshrc``), dynamically at runtime with the ``xontrib`` command, or its Python API.

Extensions are loaded via the ``xontrib load`` command.
This command may be run from anywhere in a `deepshrc <deepshrc.rst>`_ file or at any point
after deepsh has started up.

.. code-block:: deepsh

    xontrib load myext mpl mypkg.show

The same can be done in Python as well

.. code-block:: python

    from deepsh.xontribs import xontribs_load
    xontribs_load(['myext', 'mpl', 'mypkg.show'])

A xontrib can be unloaded from the current session using ``xontrib unload``

.. code-block:: deepsh

    xontrib unload myext mpl mypkg.show

Xontribs can use `setuptools entrypoints <https://setuptools.pypa.io/en/latest/userguide/entry_point.html?highlight=entrypoints>`_
to mark themselves available for autoloading using the below format.

.. code-block:: ini

    [options.entry_points]
    deepsh.xontribs =
        xontrib_name = path.to.the.module

Here the module should contain ``_load_xontrib_`` function as described above.

.. note::

    Please make sure that importing the xontrib module and calling ``_load_xontrib_`` is fast enough.
    Otherwise it will affect the shell's startup time.
    Any other imports or heavy computations should be done in lazy manner whenever possible.


Listing Known Xontribs
======================
In addition to loading extensions, the ``xontrib`` command also allows you to
list the installed xontribs. This command will report if they are loaded
in the current session. To display this
information, pass the ``list`` action to the ``xontrib`` command:

.. code-block:: deepshcon

    >>> xontrib list
    mpl     not-loaded
    myext   not-loaded


For programmatic access, you may also have this command print a JSON formatted
string:

.. code-block:: deepshcon

    >>> xontrib list --json mpl
    {"mpl": {"loaded": false, "installed": true}}

Authoring Xontribs
==================
Writing a xontrib is as easy as writing a deepsh or Python file and sticking
it in a directory named ``xontrib/``. However, please do not place an
``__init__.py`` in the ``xontrib/`` directory. It is an
*implicit namespace package* and should not have one. See
`PEP 420 <https://www.python.org/dev/peps/pep-0420/>`_ for more details.

.. warning::

    Do not place an ``__init__.py`` in the ``xontrib/`` directory!

If you plan on using ``*.xsh`` files in you xontrib, then you'll
have to add some hooks to distutils, setuptools, pip, etc. to install these
files. Try adding entries like the following entries to your ``setup()`` call
in your ``setup.py``:

.. code-block:: python

    try:
        from setuptools import setup
    except ImportError:
        from distutils.core import setup

    setup(...,
          packages=[..., 'xontrib'],
          package_dir={..., 'xontrib': 'xontrib'},
          package_data={..., 'xontrib': ['*.xsh']},
          ...)

Something similar can be done for any non-xontrib package or sub-package
that needs to distribute ``*.xsh`` files.


Tell Us About Your Xontrib!
===========================
We request that you register your xontrib with us.
We think that will make your contribution more discoverable.

To register a xontrib, create a ``PullRequest`` at
`Awesome-xontribs <https://github.com/deepsh/awesome-xontribs>`_
repository. Also, if you use Github to host your code,
please add `deepsh <https://github.com/topics/deepsh>`_ and `xontrib <https://github.com/topics/xontrib>`_
to the topics.

All of this let's users know that your xontrib is out there, ready to be used.
Of course, you're under no obligation to register your xontrib.  Users will
still be able to load your xontrib, as long as they have it installed.

Go forth!
