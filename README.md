# Falca

Falca is an intuitive REST APIs framework based on the falcon framework.

:warning: _**Production ready soon!**_ :construction:

Goals of this project:

- [x] Validates request body based on type hints.
- [x] Marshmallow support as default object serialization and deserialization
- [x] Request body mapping
- [x] Nested routers
- [ ] Plugin support
- [x] Settings (Global Configuration) support
- [x] Async Support
- [ ] OpenAPI (Swagger & Redoc)
- [x] CLI

The project design planning has been described in [DESIGN.md](https://github.com/aprilahijriyan/falca/blob/d72c3e0570975e6960a1586ba0defe5b132f1963/DESIGN.md).

Also, if you want to contribute like bug fixes, feature additions, etc. Please read our [contribution guidelines](https://github.com/aprilahijriyan/falca/blob/main/CONTRIBUTING.md) first.

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
from falca.app import ASGI
from falca.resource import Resource
from falca.responses import JSONResponse
from falca.schema import Schema
from falca.annotations import Query
from marshmallow import fields

class LimitOffsetSchema(Schema):
    limit = fields.Int()
    offset = fields.Int()

LimitOffsetQuery = Query(LimitOffsetSchema())

class Simple(Resource):
    async def on_get(self, query: LimitOffsetQuery):
        data = query.data
        if not data:
            data = {"message": "Looks good?"}

        return JSONResponse(data)

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
