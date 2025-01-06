Run Control File
=========================
Deepsh allows you to customize your shell behavior with run control files, called "deepshrc" files.
These files are written either in the Deepsh language (a superset of Python) or in Python and are executed
exactly once at startup.

The control file usually contains:

* Assignment statements setting `environment variables <envvars.html>`_. This includes standard OS environment variables that affect other programs and many that Deepsh uses for itself.
* ``contrib`` commands to load selected add-ins (`contribs <tutorial_contrib.html#loading-contribs>`_).
* Deepsh function definitions.
* `Alias definitions <aliases.html>`_, many of which invoke the above functions with specified arguments.

First of all, you need to know about the home directory ``~/.deepshrc`` control file. This file is commonly used to put configurations for the user interactive prompt and it is executed automatically only for interactive Deepsh sessions.

There are also a few places where Deepsh looks for run control files. These files will be executed automatically in both interactive and non-interactive modes, and you need to use the `$DEEPSH_INTERACTIVE <envvars.html#deepsh-interactive>`_ and `$DEEPSH_LOGIN <envvars.html#deepsh-login>`_ environment variables to determine what code you want to execute in each mode. Here is the list of run control files and directories:

* Cross-desktop group (XDG) compliant ``~/.config/deepsh/rc.xsh`` control file.
* The system-wide control file ``/etc/deepsh/deepshrc`` for Linux and OSX and in ``%ALLUSERSPROFILE%\deepsh\deepshrc`` on Windows. It controls options that are applied to all users of Deepsh on a given system.
* The home-based directory ``~/.config/deepsh/rc.d/`` and system ``/etc/deepsh/rc.d/`` can contain ``.xsh`` or ``.py`` files. They will be executed at startup in order. This allows for drop-in configuration where your configuration can be split across scripts and common and local configurations more easily separated.

In addition:

* Use ``deepsh --no-rc`` to prevent using control files.
* Use ``deepsh --rc snail.xsh`` to run only a certain control file.
* Use ``deepsh -i script.xsh`` to run deepsh in interactive mode with loading all possible control files.
* Use ``deepsh --rc rc1.xsh rc2.xsh -- script.xsh`` to run scripts with multiple control files.
* You can create autoloadable `contrib <tutorial_contrib.html#loading-contribs>`_ as alternative to run control file and reuse it as python package.

The options set per user override settings in the system-wide control file.

Deepsh provides 2 wizards to create your own "deepshrc".  ``config web`` provides basic settings, and ``config wizard``
steps you through all the available options.

config web
-----------

This helps you choose a color theme, customized prompt and add-in packages ("contribs").  It
initializes your personal run control file (usually at ``~/.deepshrc``).  To invoke it (from a deepsh prompt):

.. code-block:: deepshcon

  >>> config web
  Web config started at 'http://localhost:8421'. Hit Ctrl+C to stop.
  127.0.0.1 - - [23/Aug/2020 15:04:39] "GET / HTTP/1.1" 200 -

This will open your default browser on a page served from a local server.  You can exit the server by typing ``Ctrl+c`` at any time.

The page has:

:Colors: shows the  color themes built into Deepsh.
  Simply click on a sample to select it.  Although color names are standardized across various terminal applications,
  their actual appearance is not and do vary widely.  Seeing is believing!
:Prompts: shows various sample prompts.  It is recommended to select one but to then edit
  the ``deepshrc`` file to further refine your prompt.
:contribs: are community-contributed add-ins often used to enhance command completion and line editing,
  but can affect any aspect of Deepsh behavior.
  Choose one or more to suit your needs but note that they will require installation of additional
  packages.  You can extend Deepsh by `writing your own contrib <tutorial_contrib.html>`_, and are invited/urged to do so!
:Save: Click to write the configuration choices to your ``~/.deepshrc``. This will add a few tagged lines to your run control file, but will not
  overwrite it completely, so you can run `config web` at any time.

config wizard
--------------

This imports settings and tools you have defined in your existing (ordinary) shell such as ``bash``.
It also walks you through setting all known environment variables and contribs
in a question-and-answer format:

.. code-block:: deepshcon

    @ config wizard

              Welcome to the deepsh configuration wizard!
              ------------------------------------------
    This will present a guided tour through setting up the deepsh static
    config file. Deepsh will automatically ask you if you want to run this
    wizard if the configuration file does not exist. However, you can
    always rerun this wizard with the config command:

        @ config wizard

    This wizard will load an existing configuration, if it is available.
    Also never fear when this wizard saves its results! It will create
    a backup of any existing configuration automatically.

    This wizard has two main phases: foreign shell setup and environment
    variable setup. Each phase may be skipped in its entirety.

    For the configuration to take effect, you will need to restart deepsh.

    '`-.,_,.-*'`-.,_,.-*'`-.,_,.-*'`-.,_,.-*'`-.,_,.-*'`-.,_,.-*'``-.,_,.-*'

    To exit the wizard at any time, press Ctrl-C.


    '`-.,_,.-*'`-.,_,.-*'`-.,_,.-*'`-.,_,.-*'`-.,_,.-*'`-.,_,.-*'`-.,_,.-*'

                          Foreign Shell Setup
                          -------------------
    The deepsh shell has the ability to interface with foreign shells such
    as Bash, or zsh (fish not yet implemented).

    For configuration, this means that deepsh can load the environment,
    aliases, and functions specified in the config files of these shells.
    Naturally, these shells must be available on the system to work.
    Being able to share configuration (and source) from foreign shells
    makes it easier to transition to and from deepsh.

    Add a new foreign shell, yes or no [default: no]? yes
    shell name (e.g. bash): bash
    interactive shell [bool, default=True]:
    login shell [bool, default=False]:
    env command [str, default='env']:
    alias command [str, default='alias']:
    extra command line arguments [list of str, default=[]]:
    safely handle exceptions [bool, default=True]:
    pre-command [str, default='']:
    post-command [str, default='']:
    foreign function command [str, default=None]:
    source command [str, default=None]: source
    Foreign shell added.

    Add a new foreign shell, yes or no [default: no]? no

    '`-.,_,.-*'`-.,_,.-*'`-.,_,.-*'`-.,_,.-*'`-.,_,.-*'`-.,_,.-*'``-.,_,.-*'

                      Environment Variable Setup
                      --------------------------
    The deepsh shell also allows you to setup environment variables from
    the static configuration file. Any variables set in this way are
    superseded by the definitions in the deepshrc or on the command line.
    Still, setting environment variables in this way can help define
    options that are global to the system or user.

    The following lists the environment variable name, its documentation,
    the default value, and the current value. The default and current
    values are presented as pretty repr strings of their Python types.

    Note: Simply hitting enter for any environment variable
    will accept the default value for that entry.

    Would you like to set env vars now, yes or no [default: no]? yes

    $ALLUSERSPROFILE

    default value:
    current value: 'C:\\ProgramData'
    >>>

    $APPDATA

    default value:
    current value: 'C:\\Users\\bobhy\\AppData\\Roaming'
    >>>

    $AUTO_CD
    Flag to enable changing to a directory by entering the dirname or
    full path only (without the cd command).
    default value: False
    current value: False
    >>>

    . . .


Real world sample deepshrc
-------------------------

The following is a real-world example of such a file.

:download:`Download deepshrc <deepshrc.xsh>`

.. include:: deepshrc.xsh
    :code: deepsh

See also `contrib-rc-awesome <https://github.com/anki-code/contrib-rc-awesome>`_.

Real world sample rc.py
-------------------------

The following is a real-world example of such a file.
This can be set by ``env DEEPSHRC=rc.py deepsh`` or ``deepsh --rc=rc.py``

:download:`Download rc.py <deepshrc.py>`

.. include:: deepshrc.py
    :code: deepsh


Snippets for deepshrc
--------------------

The following are useful snippets and code that tweaks and adjust deepsh in various ways.
If you have any useful tricks, feel free to share them.

Adjust how git branch label behaves
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Deepsh adds a colored branch name to the prompt when working with git or hg repositories.
This behavior can be controlled with the ``$PROMPT`` environment variable. See how to `customize the prompt`_ .
The branch name changes color if the work dir is dirty or not. This is controlled by the ``{branch_color}`` formatter string.


The following snippet reimplements the formatter also to include untracked files when considering if a git directory is dirty.

.. code-block:: deepshcon

    from deepsh.prompt.vc import git_dirty_working_directory
    $PROMPT_FIELDS['branch_color'] = lambda: ('{BOLD_INTENSE_RED}'
                                                   if git_dirty_working_directory(include_untracked=True)
                                                   else '{BOLD_INTENSE_GREEN}')


.. _customize the prompt: tutorial.html#customizing-the-prompt


Get better colors from the ``ls`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The colors of the ``ls`` command may be hard to read in a dark terminal. If so, this is an excellent addition to the deepshrc file.

.. code-block:: deepshcon

    $LS_COLORS='rs=0:di=01;36:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:'

Make JSON data directly pastable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
With the following snippet, deepsh will understand JSON data such as ``{ "name": "Tyler", "active": false, "age": null }``.
Note that, though practical, this is rather hacky and might break other functionality. Use at your own risk.

.. code-block:: deepshcon

    import builtins
    builtins.true = True
    builtins.false = False
    builtins.null = None

Display different date information every 10th time
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For a compact shell prompts, some people prefer a very condensed time format. But when you have a lengthy shell session you might want the date to show up in your logs every now and then...

.. code-block:: deepshcon

    import time
    def get_shelldate():
        get_shelldate.fulldate %= 10
        get_shelldate.fulldate += 1
        if get_shelldate.fulldate == 1:
            return time.strftime('%d%m%Y')
        return time.strftime('%H:%M')
    get_shelldate.fulldate = 0

    $PROMPT_FIELDS['shelldate'] = get_shelldate
