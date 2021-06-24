# Falca

![Logo](https://raw.githubusercontent.com/aprilahijriyan/falca/main/falca.png)

![PyPI - Downloads](https://img.shields.io/pypi/dm/falca?color=yellow&logo=python) ![PyPI](https://img.shields.io/pypi/v/falca?color=yellow&logo=python) ![Scrutinizer code quality (GitHub/Bitbucket)](https://img.shields.io/scrutinizer/quality/g/aprilahijriyan/falca/main?logo=scrutinizer) ![Black Formatter](https://img.shields.io/badge/code%20style-black-000000.svg)

<p align="center">
Falca is an intuitive REST APIs framework.<br>
Powered by https://falconframework.org/.<br><br>
:warning: <i><strong>Production ready soon!</strong></i> :construction:<br>
</p>

Goals of this project:

* Validates request body based on type hints.
* (Pydantic & Marshmallow) support as object serialization and deserialization
* Request body mapping
* Nested routers
* Plugin support
* Settings (Global Configuration) support
* Async Support
* Routing sub-application
* CLI
* Dependency injection
* Resource shortcut (`get`, `post`, `put`, `delete`, `websocket`, etc)

# Contribution

**Do not hesitate!**

if you want to contribute like bug fixes, feature additions, etc. Please read our [contribution guidelines](https://github.com/aprilahijriyan/falca/blob/main/CONTRIBUTING.md).

# Installation

Using `pip`:

```
pip install falca
```

Alternatively, clone this repository and go to the `falca` directory:

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
from falca.responses import JSONResponse
from falca.serializers.pydantic import Schema


class LimitOffsetSchema(Schema):
    limit: Optional[int]
    offset: Optional[int]

class Simple:
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
