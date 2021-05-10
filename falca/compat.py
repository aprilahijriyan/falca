"""
Reference: https://pythonspeed.com/articles/faster-json-library/
"""

try:
    import orjson as json

    _dumps = json.dumps

    def dumps(*args, **kwds):
        option = kwds.get("option")
        if not option:
            option = json.OPT_NON_STR_KEYS
        kwds["option"] = option
        return _dumps(*args, **kwds).decode()

    json.dumps = dumps

except ImportError:
    try:
        import rapidjson as json

    except ImportError:
        import json
