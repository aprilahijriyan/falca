"""
Reference: https://pythonspeed.com/articles/faster-json-library/
"""

try:
    import orjson as json

    _dumps = json.dumps

    def dumps(*args, **kwds):
        return _dumps(*args, **kwds).decode()

    json.dumps = dumps

except ImportError:
    try:
        import rapidjson as json

    except ImportError:
        import json
