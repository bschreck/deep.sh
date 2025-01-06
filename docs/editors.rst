
======================
Editor and IDE Support
======================

Sublime Text
============
There is a `deepsh package`_ for **Sublime Text 4** (build > 4075). To install:

- Via **Package Control**: open (``^``/``⌘`` ``⇧`` ``P``) ``Command Palette`` → ``Package Control: Install Package`` → ``deepsh``
- **Manually**: clone the repository to your `Sublime Text packages`_ directory and rename it to ``deepsh``

  .. code-block:: sh

    cd /path/to/sublime/packages/directory
    git clone https://github.com/eugenesvk/sublime-deepsh.git
    mv sublime-deepsh deepsh

.. _deepsh package: https://packagecontrol.io/packages/deepsh
.. _Sublime Text packages: https://www.sublimetext.com/docs/packages.html


Visual Studio Code (VS Code)
============================
There is `deepsh extension for VS Code`_. To install search "deepsh" using extensions
menu or just press ``F1`` and run without `>` preceding:

.. code-block::

    ext install jnoortheen.deepsh

.. https://github.com/microsoft/vscode/issues/200374

Since version 1.86 of VS Code, the editor also supports loading the environment for users with deepsh as their default shell.

.. _deepsh extension for VS Code: https://marketplace.visualstudio.com/items?itemName=jnoortheen.deepsh


Emacs
=====

Emacs Deepsh mode
----------------

There is an emacs mode for editing deepsh scripts available from the
`MELPA repository`_. If you are not familiar see the installation
instructions there.

Then just add this line to your emacs configuration file:

.. code-block:: emacs-lisp

    (require 'deepsh-mode)


.. _MELPA repository: https://melpa.org/#/deepsh-mode


Deepsh Comint buffer
-------------------

You can use deepsh as your `interactive shell in Emacs
<https://www.gnu.org/software/emacs/manual/html_node/emacs/Interactive-Shell.html>`_
in a Comint buffer. This way you keep all the Emacs editing power
in the shell, but you lose deepsh's completion feature.

Make sure you install deepsh with readline support and in your
``.deepshrc`` file define

.. code-block:: deepsh

    $SHELL_TYPE = 'readline'

Also, in Emacs set ``explicit-shell-file-name`` to your deepsh executable.

Deepsh Ansi-term buffer
----------------------

The second option is to run deepsh in an Ansi-term buffer inside
Emacs. This way you have to switch modes if you want do Emacs-style
editing, but you keep deepsh's impressive completion.

For this it is preferred to have deepsh installed with the
prompt-toolkit. Then you can leave ``$SHELL_TYPE`` at its default.

Emacs will prompt you for the path of the deepsh executable when you
start up ``ansi-term``.

Vim
===

There is `deepsh syntax file for vim`_. To install run:

.. code-block::

    git clone --depth 1 https://github.com/linkinpark342/deepsh-vim ~/.vim

.. _deepsh syntax file for vim: https://github.com/linkinpark342/deepsh-vim
