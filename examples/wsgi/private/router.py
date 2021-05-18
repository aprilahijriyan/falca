from falca.responses import JSONResponse
from falca.router import Router

private_router = Router(url_prefix="/private")


@private_router.get("/users")
def on_get():
    """
    Get a secret user list
    """

    return JSONResponse(
        {
            "users": [
                {"email": "wakwaw@wkwk.com", "password": "123"},
                {"email": "admin@wkwk.com", "password": "1234"},
                {"email": "toktokpaket@wkwk.com", "password": "12345"},
            ]
        }
    )
