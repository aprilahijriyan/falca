"""
Reference: https://pythonspeed.com/articles/faster-json-library/
"""

from functools import partial

try:
    from pydantic import BaseModel as PydanticSchema
except ImportError:
    PydanticSchema = None


def _json_default(o: object):
    if PydanticSchema is not None and isinstance(o, PydanticSchema):
        return o.dict()
    raise ValueError(f"unknown object {o!r}")


try:
    import orjson as json

    _dumps = json.dumps

    def dumps(*args, **kwds):
        option = kwds.get("option")
        if not option:
            option = json.OPT_NON_STR_KEYS
        kwds["option"] = option
        return _dumps(*args, **kwds).decode()


except ImportError:
    try:
        import rapidjson as json

        dumps = json.dumps

    except ImportError:
        import json

        dumps = json.dumps

json.dumps = partial(dumps, default=_json_default)
