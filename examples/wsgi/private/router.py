from falca.router import Router

from .resources.user import User

private_router = Router(url_prefix="/private")
private_router.add_route("/users", User())
