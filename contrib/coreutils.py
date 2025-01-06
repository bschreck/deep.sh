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
from deepsh.xoreutils.cat import cat
from deepsh.xoreutils.echo import echo
from deepsh.xoreutils.pwd import pwd
from deepsh.xoreutils.tee import tee
from deepsh.xoreutils.tty import tty
from deepsh.xoreutils.umask import umask
from deepsh.xoreutils.uname import uname
from deepsh.xoreutils.uptime import uptime
from deepsh.xoreutils.yes import yes


def _load_xontrib_(xsh: DeepshSession, **_):
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
        from deepsh.xoreutils.ulimit import ulimit

        xsh.aliases["ulimit"] = ulimit
