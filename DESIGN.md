# Architectural Design

This is the roadmap of the Falca Framework project. There are many tasks that we will be working on, below is the workflow.

# Application

The falcon application itself is designed to be as minimal as possible and we will add some functionality to it, such as:

* `Settings`

    A place where you can store global configurations such as frameworks (django, flask, etc).

* `Plugins`

    Support for creating plugins.
    Yeah, this is a little confusing. But you can access installed plugins to all **Resources** via the `falca.decorators.use_plugins` decorator. I think this is the best way. :)

* `Router`

    We plan to add some features to the default Router from the falcon framework, already implemented in the `main` branch. These are the features we've added:

    - `Nested Routers`

        It is similar to Blueprint in the flask framework, but it is more minimal.

* `Static Files`

    By default the endpoint for serving static files is appended to the `/static` endpoint and serves the file depending on the `static` folder in the **root path of the application**. It's like a flask.

* `Templates`

    By default for rendering html templates, we use mako as the template engine. The directory for templates is located in the `templates` folder in the **root path of the application**. It's like a flask.


# Global Attributes

In some frameworks like flask there is a global variable `current_app` which is a local proxy that can be used when the flask context app has been pushed. However, in the falcon framework is very confusing, to add functionality like that. This is the best idea I have in mind :). We will add some attributes to the resource via middleware. These are the attributes that will be added:

* `request.context.app` => App instance object.
* `request.context.templates` => Mako template lookup.
* `self.request` => falcon.Request object
* `self.response` => falcon.Response object

That `self` is the instance of your Resource object.

# Request & Response

By default, the request and response objects that are passed to the responder are removed and moved to the `self.request` and `self.response` attributes. See [here](#global-attributes)

To return a response you can use the `html()` or `json()` methods found in Resources.

# Request Body

Falca handles the request body a little more aesthetic xD. You can handle query, body, forms, files and headers using the notations `Query`, `Body`, `Form`, `File`, `Header` in` falca.annotations`.

For examples you can find them in [examples/](https://github.com/aprilahijriyan/falca/tree/main/examples/) directory.

# Project Layouts

You can find the project layout in the [examples/](https://github.com/aprilahijriyan/falca/tree/main/examples/) directory.

# CLI

This feature is similar to the flask command line. Maybe the name for the command is **falca**.

The features that will be in this command are:

* Support for running applications
* Support to display a list of endpoint
* Support for adding commands via [entry_points](https://setuptools.readthedocs.io/en/latest/userguide/entry_point.html)
