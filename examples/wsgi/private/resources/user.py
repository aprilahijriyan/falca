from falca.resource import Resource


class User(Resource):
    def on_get(self):
        """
        Get a secret user list
        """

        self.json(
            {
                "users": [
                    {"email": "wakwaw@wkwk.com", "password": "123"},
                    {"email": "admin@wkwk.com", "password": "1234"},
                    {"email": "toktokpaket@wkwk.com", "password": "12345"},
                ]
            }
        )
