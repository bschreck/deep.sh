"""Additional core utilities that are implemented in deepsh.

The current list includes:

* cat
* echo
* pwd
* tee
* tty
* yes

In many cases, these may have a lower performance overhead than the
posix command line utility with the same name. This is because these
tools avoid the need for a full subprocess call. Additionally, these
tools are cross-platform.
"""

from deepsh.built_ins import DeepshSession
from deepsh.platform import ON_POSIX
from deepsh.coreutils.cat import cat
from deepsh.coreutils.echo import echo
from deepsh.coreutils.pwd import pwd
from deepsh.coreutils.tee import tee
from deepsh.coreutils.tty import tty
from deepsh.coreutils.umask import umask
from deepsh.coreutils.uname import uname
from deepsh.coreutils.uptime import uptime
from deepsh.coreutils.yes import yes


def _load_contrib_(xsh: DeepshSession, **_):
    xsh.aliases["cat"] = cat
    xsh.aliases["echo"] = echo
    xsh.aliases["pwd"] = pwd
    xsh.aliases["tee"] = tee
    xsh.aliases["tty"] = tty
    xsh.aliases["uname"] = uname
    xsh.aliases["uptime"] = uptime
    xsh.aliases["umask"] = umask
    xsh.aliases["yes"] = yes
    if ON_POSIX:
        from deepsh.coreutils.ulimit import ulimit

        xsh.aliases["ulimit"] = ulimit
