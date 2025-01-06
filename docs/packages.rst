Package Manager
===============

You can install deepsh using ``conda``, ``pip`` or the package manager for
your operating system distribution.

For the fullest interactive user experience, these additional packages should also be installed:

  :prompt-toolkit: for command completion, configurable key bindings and especially multi-line line editing.
  :pygments: for deepsh and Python syntax-specific highlighting
  :setproctitle: updates process title (in terminal window and process monitor) to match Deepsh arguments.

Installing with these packages is the recommended configuration and is documented first.
If you are operating in a specialized or restricted environment, you can install just the deepsh package, as
described in `fewer prerequisites`_


**conda:**

.. code-block:: console

    $ conda config --add channels conda-forge
    $ conda install deepsh


**pip:** Typically you will activate a virtual environment and install deepsh there.  This will ensure that you invoke the
correct Python interpreter and ``pip`` module.

.. code-block:: console

    $ pip install 'deepsh[full]'

This uses the pip 'extras' syntax, and is equivalent to:

.. code-block:: console

    $ pip install pygments prompt-toolkit setproctitle deepsh

The above ``pip`` commands may have to be spelled ``pip3`` or ``sudo pip3`` if you are not installing in a virtual environment.

**source:** Pip can also install the most recent deepsh source code from the
`deepsh project repository <https://github.com/deepsh/deepsh>`_.

.. code-block:: console

    $ pip install pygments prompt-toolkit setproctitle https://github.com/deepsh/deepsh/archive/main.zip

Spelling of ``pip`` command may likewise have to be amended as noted above.

**core shell:** When using ``deepsh`` as a default shell (and we do!), it's important to ensure that it is installed in a
Python environment that is independent of changes from the system package manager.  If you are installing
``deepsh`` via your system package-manager, this is handled for you.  If you install ``deepsh`` outside of your
system package manager, you can use `deepsh-install <a href="https://github.com/anki-code/deepsh-install>`_ for this.

**platform package managers**
Various operating system distributions have platform-specific package managers which may offer a deepsh package.
This may not be  the most current version of deepsh, but it should have been tested for stability on that platform
by the distribution managers.


   +---------------------------+-----------------------------+---------------------+
   | OS or distribution        |  command                    |   Package(s)        |
   +===========================+=============================+=====================+
   | Debian/Ubuntu             | ``$ [sudo] apt install``    |                     |
   +---------------------------+-----------------------------+    pygments         |
   | Fedora                    | ``$ [sudo] dnf install``    |    prompt-toolkit   |
   +---------------------------+-----------------------------+    setproctitle     |
   | Arch Linux                | ``$ [sudo] pacman -S``      |    deepsh            |
   +---------------------------+-----------------------------+                     |
   | OSX                       | ``$ [sudo] brew install``   |                     |
   +---------------------------+-----------------------------+---------------------+


If you run into any problems, please let us know!

Fewer Prerequisites
--------------------

A design goal of Deepsh is to run in any environment that supports a (supported) Python interpreter, you
can install just the ``deepsh`` package (using any package manager).

.. code-block:: console

    pip install deepsh

When it starts up, if deepsh does not find ``pygments`` or ``setproctitle`` packages, it simply does not colorize
or highlight syntax or set process title, respectively.

If it does not find ``prompt-toolkit`` package, it will
use the Python ``readline`` module (which reads configuration  file ``.inputrc`` in a manner compatible with ``GNU readline``).
To ensure deepsh uses ``readline`` even if ``prompt-toolkit`` is installed, configure this in your
`deepshrc <deepshrc.rst>`_ (e.g. ``~/.deepshrc``) file:

.. code-block:: deepshcon

    $SHELL_TYPE = 'readline'

Windows
-------

On Windows 10, the separately-installable `Windows Terminal app`_ is recommended.

.. _`Windows Terminal app`: platform-issues.html#windows-terminal
