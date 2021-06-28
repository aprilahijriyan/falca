from falca.helpers import abort, get_argnotations


def test_abort(wsgi_app, wsgi_client):
    @wsgi_app.get("/404")
    def handler404():
        abort(404)

    resp = wsgi_client.get("/404")
    assert resp.json == {
        "status": {"code": 404, "description": "Not Found"},
        "link": None,
    }


def test_get_argnotations():
    def valid_func(a: int = 1, b=2):
        pass

    n = get_argnotations(valid_func)
    assert n == {"a": int}
