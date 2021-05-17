import asyncio

from falca.resource import Resource
from falca.responses import JsonResponse


class User(Resource):
    async def on_get(self):
        await asyncio.sleep(5)
        return JsonResponse(
            {
                "users": [
                    {"email": "wakwaw@wkwk.com", "password": "123"},
                    {"email": "admin@wkwk.com", "password": "1234"},
                    {"email": "toktokpaket@wkwk.com", "password": "12345"},
                ]
            }
        )
