import asyncio

from falca.responses import JSONResponse


class User:
    async def on_get(self):
        await asyncio.sleep(5)
        return JSONResponse(
            {
                "users": [
                    {"email": "wakwaw@wkwk.com", "password": "123"},
                    {"email": "admin@wkwk.com", "password": "1234"},
                    {"email": "toktokpaket@wkwk.com", "password": "12345"},
                ]
            }
        )
