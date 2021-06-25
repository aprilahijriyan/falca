# Changelog

## v1.0.0 (2021-06-19)

### ✨ New

* Plugin support (close #2) [aprilahijriyan]

* Add dependency 'Settings' [aprilahijriyan]

* Add exception handling specifics for marshmallows and pydantic. [aprilahijriyan]

* Dependency injection support. [aprilahijriyan]

* Support command overwrite via app.cli. [aprilahijriyan]

* Added TextResponse, StreamingResponse and StreamingVideoResponse. [aprilahijriyan]

* Add AsyncRouter to ASGI (so it's clearer) [aprilahijriyan]

* Add shell command. [aprilahijriyan]

* Settings support (close #3) [aprilahijriyan]

* Add client for testing. [aprilahijriyan]

* Load command from entry_points. [aprilahijriyan]

* CLI support. [aprilahijriyan]

* Add file upload example. [aprilahijriyan]

* Add example static file & html response. [aprilahijriyan]

* Add more examples. [aprilahijriyan]

### 🎨 Improved

* Support passing marshmallow schema objects instead of instance. [aprilahijriyan]

* Remove resource class (not useful) [aprilahijriyan]

* Remove unused TestCase class. [aprilahijriyan]

* Add new logo. [aprilahijriyan]

* Add more type hints. [aprilahijriyan]

* Add a websocket shortcut to AsyncRouter. [aprilahijriyan]

* Support for creating function-based resources on App and Router objects. [aprilahijriyan]

* Rename response class and routing. [aprilahijriyan]

* Rename the response class. [aprilahijriyan]

* Added endpoint conflict check & invalid router. [aprilahijriyan]

* Update the app. [aprilahijriyan]

* Add more example. [aprilahijriyan]

* Use our clients to test. [aprilahijriyan]

* Async support. Close #4. [aprilahijriyan]

* Add an asterisk to the save() method. [aprilahijriyan]

* Remove unused files. [aprilahijriyan]

### 🐛 Fix

* Example code. [aprilahijriyan]

* Resolution. [aprilahijriyan]

* Logo project. [aprilahijriyan]

* Markdown format inside html. [aprilahijriyan]

* Rename the response class. [aprilahijriyan]

* Typer nesting command support. [aprilahijriyan]

* Ensure that the 'self' parameter is not duplicated in the view. [aprilahijriyan]

* Websocket support and testing. [aprilahijriyan]

* Allow without context. [aprilahijriyan]

* Change behavior of handling Request and Response based on #7. [aprilahijriyan]

* Nested routers. [aprilahijriyan]

* Add information if running with wsgiref. [aprilahijriyan]

* Do not overwrite the Form Parser Middleware result (async) [aprilahijriyan]

* Do not overwrite FormParserMiddleware results. [aprilahijriyan]

* Find recursive routers. [aprilahijriyan]

* Multipart form data. [aprilahijriyan]

* Cache plugin inside responder. [aprilahijriyan]

* Fix middleware (parse forms, json & files) [aprilahijriyan]

* Plugin feature. [aprilahijriyan]

* Response content (based on media_handlers) [aprilahijriyan]

* Marshmallow keys (int -> str) [aprilahijriyan]

### ✔️ Tests

* Added endpoint conflict tests. [aprilahijriyan]

* Add test request x-www-form-urlencoded & responder documents. [aprilahijriyan]

### 📖 DOC

* Prepare first release. [aprilahijriyan]

* Added AUTHORS.md. [aprilahijriyan]

* Add logo. [aprilahijriyan]

* Add new features & update examples. [aprilahijriyan]

* Add usage examples. [aprilahijriyan]

* Settings support. [aprilahijriyan]

* Add description. [aprilahijriyan]

* Add more details of the project. [aprilahijriyan]

* CLI Support. [aprilahijriyan]

* Async support. [aprilahijriyan]

* Nested router support. [aprilahijriyan]

* Add an example of nesting router. [aprilahijriyan]

* Add readme. [aprilahijriyan]

### Other

* Create config.yml. [Aprila Hijriyan]

* Update issue templates. [Aprila Hijriyan]

* Create CODE_OF_CONDUCT.md. [Aprila Hijriyan]

* Create python-publish.yml. [Aprila Hijriyan]

* ➖ Removing unused module. [aprilahijriyan]

* ✨ Feature: Resource support in a style like function. [aprilahijriyan]

* 💩 Needs Improvement:  For multiple nested routers, not implemented yet. [aprilahijriyan]

* Make it clearer on the addition of the endpoint and router nesting. [aprilahijriyan]

* ➕ Adding Dependency:  httpie. [aprilahijriyan]

* ⚡ General Update:  cache plugin. [aprilahijriyan]

* ⚡ General Update:  Added parameter notation. [aprilahijriyan]

## v2.2.0 (2021-06-26)

### ✨ New

* Support group command merging and importing functions via the FALCA_APP env. [aprilahijriyan]

* Support for mounting sub-application. [aprilahijriyan]

* Support adding function resources to add_route. [aprilahijriyan]

* Support installing plugins via objects. [aprilahijriyan]

### 🎨 Improved

* Code optimization from the scrutinizer-ci report. [aprilahijriyan]

* Added FileResponse and improved template rendering in HTMLResponse. [aprilahijriyan]

### 🐛 Fix

* Update major version (due to commit 70d309740b9f93076ad290afca3762deb24696e6) [aprilahijriyan]

* Separate 'method' argument to keyword argument. [aprilahijriyan]

* Pydantic validation error message. [aprilahijriyan]

### ✔️ Tests

* Cli. [aprilahijriyan]

* Responses. [aprilahijriyan]

### 📖 DOC

* Add more badges. [aprilahijriyan]

* Added badges and minor fixes. [aprilahijriyan]

* Add unreleased features. [aprilahijriyan]

* Add pip installation guide. [aprilahijriyan]
