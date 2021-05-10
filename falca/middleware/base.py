from falcon.app import App
from falcon.request import Request
from falcon.response import Response


class Middleware(object):
    """Middleware Component.

    rfc: https://falcon.readthedocs.io/en/0.3.0.1/api/middleware.html#middleware-components
    """

    def __init__(self, app: App = None) -> None:
        self.app = app
        super().__init__()

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
