.. _tutorial_contrib:

************************************
Tutorial: Extensions (Contribs)
************************************
Take a deep breath and prepare for some serious Show & Tell; it's time to
learn about deepsh extensions!

Deepsh comes with some default set of extensions. These can be viewed :py:mod:`here <contrib>`.

Also checkout the list of `Awesome Contributions <https://deepsh.github.io/awesome-contribs/>`_
from the community.

Overview
========
Contributions, or ``contribs``, are a set of tools and conventions for
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
Contribs are modules with some special functions written
in either deepsh (``*.xsh``) or Python (``*.py``).

Here is a template:

.. code-block:: python

    from deepsh.built_ins import DeepshSession

    def _load_contrib_(xsh: DeepshSession, **kwargs) -> dict:
        """
        this function will be called when loading/reloading the contrib.

        Args:
            xsh: the current deepsh session instance, serves as the interface to manipulate the session.
                 This allows you to register new aliases, history backends, event listeners ...
            **kwargs: it is empty as of now. Kept for future proofing.
        Returns:
            dict: this will get loaded into the current execution context
        """

    def _unload_contrib_(xsh: DeepshSession, **kwargs) -> dict:
        """If you want your extension to be unloadable, put that logic here"""

This _load_contrib_() function is called after your extension is imported,
and the currently active :py:class:`deepsh.built_ins.DeepshSession` instance is passed as the argument.

.. note::

    Contribs without ``_load_contrib_`` are still supported.
    But when such contrib is loaded, variables listed
    in ``__all__`` are placed in the current
    execution context if defined.

Normally, these are stored and found in an
`implicit namespace package <https://www.python.org/dev/peps/pep-0420/>`_
called ``contrib``. However, contribs may be placed in any package or directory
that is on the ``$PYTHONPATH``.

If a module is in the ``contrib`` namespace package, it can be referred to just
by its module name. If a module is in any other package, then it must be
referred to by its full package path, separated by ``.`` like you would in an
import statement.  Of course, a module in ``contrib`` may be referred to
with the full ``contrib.myext``. But just calling it ``myext`` is a lot shorter
and one of the main advantages of placing an extension in the ``contrib``
namespace package.

Here is a sample file system layout and what the contrib names would be::

    |- contrib/
       |- javert.xsh     # "javert", because in contrib
       |- your.py        # "your",
       |- eyes/
          |- __init__.py
          |- scream.xsh  # "eyes.scream", because eyes is in contrib
    |- mypkg/
       |- __init__.py    # a regular package with an init file
       |- other.py       # not a contrib
       |- show.py        # "mypkg.show", full module name
       |- tell.xsh       # "mypkg.tell", full module name
       |- subpkg/
          |- __init__.py
          |- done.py     # "mypkg.subpkg.done", full module name


You can also use the `contrib template <https://github.com/deepsh/contrib-cookiecutter>`_ to easily
create the layout for your contrib package.


Loading Contribs
================
Contribs may be loaded in a few different ways: from the `deepshrc <deepshrc.rst>`_ file
(e.g. ``~/.deepshrc``), dynamically at runtime with the ``contrib`` command, or its Python API.

Extensions are loaded via the ``contrib load`` command.
This command may be run from anywhere in a `deepshrc <deepshrc.rst>`_ file or at any point
after deepsh has started up.

.. code-block:: deepsh

    contrib load myext mpl mypkg.show

The same can be done in Python as well

.. code-block:: python

    from deepsh.contribs import contribs_load
    contribs_load(['myext', 'mpl', 'mypkg.show'])

A contrib can be unloaded from the current session using ``contrib unload``

.. code-block:: deepsh

    contrib unload myext mpl mypkg.show

Contribs can use `setuptools entrypoints <https://setuptools.pypa.io/en/latest/userguide/entry_point.html?highlight=entrypoints>`_
to mark themselves available for autoloading using the below format.

.. code-block:: ini

    [options.entry_points]
    deepsh.contribs =
        contrib_name = path.to.the.module

Here the module should contain ``_load_contrib_`` function as described above.

.. note::

    Please make sure that importing the contrib module and calling ``_load_contrib_`` is fast enough.
    Otherwise it will affect the shell's startup time.
    Any other imports or heavy computations should be done in lazy manner whenever possible.


Listing Known Contribs
======================
In addition to loading extensions, the ``contrib`` command also allows you to
list the installed contribs. This command will report if they are loaded
in the current session. To display this
information, pass the ``list`` action to the ``contrib`` command:

.. code-block:: deepshcon

    >>> contrib list
    mpl     not-loaded
    myext   not-loaded


For programmatic access, you may also have this command print a JSON formatted
string:

.. code-block:: deepshcon

    >>> contrib list --json mpl
    {"mpl": {"loaded": false, "installed": true}}

Authoring Contribs
==================
Writing a contrib is as easy as writing a deepsh or Python file and sticking
it in a directory named ``contrib/``. However, please do not place an
``__init__.py`` in the ``contrib/`` directory. It is an
*implicit namespace package* and should not have one. See
`PEP 420 <https://www.python.org/dev/peps/pep-0420/>`_ for more details.

.. warning::

    Do not place an ``__init__.py`` in the ``contrib/`` directory!

If you plan on using ``*.xsh`` files in you contrib, then you'll
have to add some hooks to distutils, setuptools, pip, etc. to install these
files. Try adding entries like the following entries to your ``setup()`` call
in your ``setup.py``:

.. code-block:: python

    try:
        from setuptools import setup
    except ImportError:
        from distutils.core import setup

    setup(...,
          packages=[..., 'contrib'],
          package_dir={..., 'contrib': 'contrib'},
          package_data={..., 'contrib': ['*.xsh']},
          ...)

Something similar can be done for any non-contrib package or sub-package
that needs to distribute ``*.xsh`` files.


Tell Us About Your Contrib!
===========================
We request that you register your contrib with us.
We think that will make your contribution more discoverable.

To register a contrib, create a ``PullRequest`` at
`Awesome-contribs <https://github.com/deepsh/awesome-contribs>`_
repository. Also, if you use Github to host your code,
please add `deepsh <https://github.com/topics/deepsh>`_ and `contrib <https://github.com/topics/contrib>`_
to the topics.

All of this let's users know that your contrib is out there, ready to be used.
Of course, you're under no obligation to register your contrib.  Users will
still be able to load your contrib, as long as they have it installed.

Go forth!
