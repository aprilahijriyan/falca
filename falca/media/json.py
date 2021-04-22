from falcon.media.json import JSONHandler as JSONHandlerBase
from falcon.media.json import JSONHandlerWS as JSONHandlerWSBase

from ..compat import json

JSONHandler = JSONHandlerBase(json.dumps, json.loads)
JSONHandlerWS = JSONHandlerWSBase(json.dumps, json.loads)
