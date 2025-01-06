"""Custom tools for managing JSON serialization / deserialization of deepsh
objects.
"""

import functools

from deepsh.tools import EnvPath


@functools.singledispatch
def serialize_deepsh_json(val):
    """JSON serializer for deepsh custom data structures. This is only
    called when another normal JSON types are not found.
    """
    return str(val)


@serialize_deepsh_json.register(EnvPath)
def _serialize_deepsh_json_env_path(val):
    return val.paths
