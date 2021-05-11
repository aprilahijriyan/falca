from falcon.app import App
from falcon.request import Request
from falcon.response import Response


class Middleware(object):
    """Middleware Component.

    rfc: https://falcon.readthedocs.io/en/0.3.0.1/api/middleware.html#middleware-components
    """

    content_type = None

    def __init__(self, app: App = None) -> None:
        self.app = app
        super().__init__()

    async def process_startup(self, scope, event):
        """Process the ASGI lifespan startup event.

        Invoked when the server is ready to start up and
        receive connections, but before it has started to
        do so.

        To halt startup processing and signal to the server that it
        should terminate, simply raise an exception and the
        framework will convert it to a "lifespan.startup.failed"
        event for the server.

        Args:
            scope (dict): The ASGI scope dictionary for the
                lifespan protocol. The lifespan scope exists
                for the duration of the event loop.
            event (dict): The ASGI event dictionary for the
                startup event.
        """

    async def process_shutdown(self, scope, event):
        """Process the ASGI lifespan shutdown event.

        Invoked when the server has stopped accepting
        connections and closed all active connections.

        To halt shutdown processing and signal to the server
        that it should immediately terminate, simply raise an
        exception and the framework will convert it to a
        "lifespan.shutdown.failed" event for the server.

        Args:
            scope (dict): The ASGI scope dictionary for the
                lifespan protocol. The lifespan scope exists
                for the duration of the event loop.
            event (dict): The ASGI event dictionary for the
                shutdown event.
        """

    def process_request(self, req: Request, resp: Response):
        """Process the request before routing it.

        Args:
            req: Request object that will eventually be
                routed to an on_* responder method.
            resp: Response object that will be routed to
                the on_* responder.
        """

    def process_resource(self, req: Request, resp: Response, resource: object, *args):
        """Process the request after routing.

        Args:
            req: Request object that will be passed to the
                routed responder.
            resp: Response object that will be passed to the
                responder.
            resource: Resource object to which the request was
                routed. May be None if no route was found for
                the request.
        """

    def process_response(self, req: Request, resp: Response, resource: object, *args):
        """Post-processing of the response (after routing).

        Args:
            req: Request object.
            resp: Response object.
            resource: Resource object to which the request was
                routed. May be None if no route was found
                for the request.
        """

    async def process_request_async(self, req: Request, resp: Response):
        pass

    async def process_resource_async(
        self, req: Request, resp: Response, resource: object, *args
    ):
        pass

    async def process_response_async(
        self, req: Request, resp: Response, resource: object, *args
    ):
        pass

    def is_valid_content_type(self, req: Request):
        if (
            self.content_type
            and req.content_type
            and self.content_type in req.content_type
        ):
            return True
        return False
