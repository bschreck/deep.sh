"""Implements the deepsh history backend."""

import collections

from deepsh.history.base import History


class DummyHistory(History):
    """A dummy implement of history backend."""

    def append(self, cmd):
        pass

    def items(self, newest_first=False):
        yield {"inp": "# dummy history backend in action", "ts": 1464652800, "ind": 0}

    def all_items(self, newest_first=False):
        return self.items(newest_first=newest_first)

    def info(self):
        data = collections.OrderedDict()
        data["backend"] = "dummy"
        data["sessionid"] = str(self.sessionid)
        return data
