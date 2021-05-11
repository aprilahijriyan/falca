from falca.router import AsyncRouter

from .resources.user import User

private_router = AsyncRouter(url_prefix="/private")
private_router.add_route("/users", User())
