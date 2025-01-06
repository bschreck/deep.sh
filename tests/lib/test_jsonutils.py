"""Testing deepsh json hooks"""

import json

import pytest

from deepsh.lib.jsonutils import serialize_deepsh_json
from deepsh.tools import EnvPath


@pytest.mark.parametrize(
    "inp",
    [
        42,
        "yo",
        ["hello"],
        {"x": 65},
        EnvPath(["wakka", "jawaka"]),
        ["y", EnvPath(["wakka", "jawaka"])],
        {"z": EnvPath(["wakka", "jawaka"])},
    ],
)
def test_serialize_deepsh_json_roundtrip(inp):
    s = json.dumps(inp, default=serialize_deepsh_json)
    obs = json.loads(s)
    assert inp == obs
