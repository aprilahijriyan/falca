from falca.resource import Resource
from falca.responses import JsonResponse


class User(Resource):
    def on_get(self):
        """
        Get a secret user list
        """

        return JsonResponse(
            {
                "users": [
                    {"email": "wakwaw@wkwk.com", "password": "123"},
                    {"email": "admin@wkwk.com", "password": "1234"},
                    {"email": "toktokpaket@wkwk.com", "password": "12345"},
                ]
            }
        )
