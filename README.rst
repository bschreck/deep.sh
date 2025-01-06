deepsh
=====

.. class:: center

    **deepsh** is a Python-powered shell. Full-featured and cross-platform. The language is a superset of Python 3.6+ with additional shell primitives.  Deepsh word was made from *conch* (🐚, *@*) and indicates belonging to the command shells world.


.. list-table::
   :widths: 1 1

   *  -  **Deepsh is the Shell**
      -  **Deepsh is Python**

   *  -  .. code-block:: shell

            cd $HOME

            id $(whoami)

            cat /etc/passwd | grep root > ~/root.txt

            $PROMPT = '@ '


      -  .. code-block:: python

            2 + 2

            var = "hello".upper()

            import json; json.loads('{"a":1}')

            [i for i in range(0,10)]

   *  -  **Deepsh is the Shell in Python**
      -  **Deepsh is Python in the Shell**

   *  -  .. code-block:: python

            len($(curl -L https://con.sh))

            $PATH.append('/tmp')

            p'/etc/passwd'.read_text().find('root')

            contrib load dalias
            id = $(@json docker ps --format json)['ID']

      -  .. code-block:: python

            name = 'foo' + 'bar'.upper()
            echo @(name) > /tmp/@(name)

            ls @(input('file: '))
            touch @([f"file{i}" for i in range(0,10)])

            aliases['e'] = 'echo @(2+2)'
            aliases['a'] = lambda args: print(args)


If you like deepsh, :star: the repo, `write a tweet`_ and stay tuned by watching releases.

.. class:: center

    .. image:: https://img.shields.io/badge/Zulip%20Community-deepsh-green
            :target: https://deepsh.zulipchat.com/join/hbvue5rimpdkwkdjuiqfs7tv/
            :alt: Join to deepsh.zulipchat.com

    .. image:: https://github.com/deepsh/deepsh/actions/workflows/test.yml/badge.svg
            :target: https://github.com/deepsh/deepsh/actions/workflows/test.yml
            :alt: GitHub Actions

    .. image:: https://codecov.io/gh/deepsh/deepsh/branch/master/graphs/badge.svg?branch=main
            :target: https://codecov.io/github/deepsh/deepsh?branch=main
            :alt: codecov.io

    .. image:: https://repology.org/badge/tiny-repos/deepsh.svg
            :target: https://repology.org/project/deepsh/versions
            :alt: repology.org


First steps
***********

Install deepsh from pip:

.. code-block:: deepshcon

    python -m pip install 'deepsh[full]'

And visit https://con.sh for more information:

- `Installation <https://con.sh/contents.html#installation>`_ - using packages, docker or AppImage.
- `Tutorial <https://con.sh/tutorial.html>`_ - step by step introduction in deepsh.

Extensions
**********

Deepsh has an extension/plugin system.  We call these additions ``contribs``.

- `Contribs on Github <https://github.com/topics/contrib>`_
- `Awesome contribs <https://github.com/deepsh/awesome-contribs>`_
- `Core contribs <https://con.sh/api/_autosummary/contribs/contrib.html>`_
- `Create a contrib step by step from template <https://github.com/deepsh/contrib-template>`_

Projects that use deepsh or compatible
*************************************

- `conda <https://conda.io/projects/conda/en/latest/>`_ and `mamba <https://mamba.readthedocs.io/en/latest/>`_: Modern package managers.
- `Starship <https://starship.rs/>`_: Cross-shell prompt.
- `zoxide <https://github.com/ajeetdsouza/zoxide>`_: A smarter cd command.
- `gitsome <https://github.com/donnemartin/gitsome>`_: Supercharged Git/shell autocompleter with GitHub integration.
- `xxh <https://github.com/xxh/xxh>`_: Using deepsh wherever you go through the SSH.
- `any-nix-shell <https://github.com/haslersn/any-nix-shell>`_: deepsh support for the ``nix run`` and ``nix-shell`` environments of the Nix package manager.
- `lix <https://github.com/lix-project/lix>`_: A modern, delicious implementation of the Nix package manager.
- `x-cmd <https://www.x-cmd.com/>`_: x-cmd is a vast and interesting collection of tools guided by the Unix philosophy.
- `rever <https://regro.github.io/rever-docs/>`_: Cross-platform software release tool.
- `Regro autotick bot <https://github.com/regro/cf-scripts>`_: Regro Conda-Forge autoticker.

Jupyter-based interactive notebooks via `contrib-jupyter <https://github.com/deepsh/contrib-jupyter>`_:

- `Jupyter and JupyterLab <https://jupyter.org/>`_: Interactive notebook platform.
- `euporie <https://github.com/joouha/euporie>`_: Terminal based interactive computing environment.
- `Jupytext <https://jupytext.readthedocs.io/>`_: Clear and meaningful diffs when doing Jupyter notebooks version control.

The deepsh shell community
*************************

The deepsh shell is developed by a community of volunteers. There are a few ways to help out:

- Solve a `popular issue <https://github.com/deepsh/deepsh/issues?q=is%3Aissue+is%3Aopen+sort%3Areactions-%2B1-desc>`_ or `high priority issue <https://github.com/deepsh/deepsh/issues?q=is%3Aopen+is%3Aissue+label%3Apriority-high+sort%3Areactions-%2B1-desc>`_ or a `good first issue <https://github.com/deepsh/deepsh/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22+sort%3Areactions-%2B1-desc>`_. You can start with the `Developer guide <https://con.sh/devguide.html>`_.
- Take an `idea <https://github.com/deepsh/contrib-template/issues?q=is%3Aopen+is%3Aissue+label%3Aidea+sort%3Areactions-%2B1-desc>`_ and `create a new contrib <https://github.com/deepsh/contrib-template#why-use-this-template>`_.
- Contribute to `deepsh API <https://github.com/deepsh/deepsh/tree/main/deepsh/api>`_.
- Become deepsh core developer by deep diving into deepsh internals. E.g. we feel a lack of Windows support.
- `Become a sponsor to deepsh <https://github.com/sponsors/deepsh>`_.
- `Write a tweet`_, post or an article to spread the good word about deepsh in the world.
- Give a star to deepsh repository and to `contribs <https://github.com/topics/contrib>`_ you like.

We welcome new contributors!

.. _write a tweet: https://twitter.com/intent/tweet?text=deepsh%20is%20a%20Python-powered,%20cross-platform,%20Unix-gazing%20shell%20language%20and%20command%20prompt.&url=https://github.com/deepsh/deepsh

Credits
*******

- Thanks to `Zulip <https://zulip.com/>`_ for supporting the deepsh community!
