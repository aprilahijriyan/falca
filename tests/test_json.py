from pydantic import BaseModel
from pytest import raises

from falca.compat import json


class Model(BaseModel):
    id: int


def test_dumps():
    d = {"n": 1, "s": Model(id=2)}
    result = json.dumps(d)
    resp = '{"n": 1, "s": {"id": 2}}'
    try:
        resp = resp.replace(" ", "")
    except ImportError:
        pass

    assert result == resp

    with raises((ValueError, TypeError)):

        class Obj:
            pass

        d["s"] = Obj()
        json.dumps(d)
