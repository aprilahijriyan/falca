# Falca

<p align="center">
<img width="100%" height="150" src="https://raw.githubusercontent.com/aprilahijriyan/falca/main/falca.jpeg">
Falca is an intuitive REST APIs framework.<br>
Powered by https://falconframework.org/.<br><br>
:warning: <i><strong>Production ready soon!</strong></i> :construction:<br>
</p>

Goals of this project:

- [x] Validates request body based on type hints.
- [x] (Pydantic & Marshmallow) support as object serialization and deserialization
- [x] Request body mapping
- [x] Nested routers
- [ ] Plugin support
- [x] Settings (Global Configuration) support
- [x] Async Support
- [ ] OpenAPI (Swagger & Redoc)
- [x] CLI
- [x] Dependency injection
- [x] Resource shortcut (`get`, `post`, `put`, `delete`, `websocket`, etc)


# Contribution

**Do not hesitate!**

if you want to contribute like bug fixes, feature additions, etc. Please read our [contribution guidelines](https://github.com/aprilahijriyan/falca/blob/main/CONTRIBUTING.md).

# Installation

Clone this repository and go to the directory:

```
git clone https://github.com/aprilahijriyan/falca
cd falca
```

Initialize the environment with python v3.7 using [poetry](https://python-poetry.org/)

```
poetry env use $(which python3.7)
```

Install dependencies

```
poetry install --no-dev
```

# Usage

Let's see how beautiful it is

```python
# app.py

from typing import Optional

from falca.app import ASGI
from falca.depends.pydantic import Query
from falca.resource import Resource
from falca.responses import JSONResponse
from falca.serializers.pydantic import Schema


class LimitOffsetSchema(Schema):
    limit: Optional[int]
    offset: Optional[int]

class Simple(Resource):
    async def on_get(self, query: dict = Query(LimitOffsetSchema)):
        return JSONResponse(query)

app = ASGI(__name__)
app.add_route("/", Simple())

```

Save the code above with filename `app.py`
And run it with the command:

```sh
falca runserver
```

**NOTE**: For the ASGI app, you need to install `uvicorn` before running it.
Also for other examples, you can find them [here](https://github.com/aprilahijriyan/falca/tree/main/examples)
