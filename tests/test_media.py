from mimetypes import guess_type

from falca.middleware.files import FileStorage
from falca.request import Request
from falca.responses import JSONResponse


def test_file_upload(wsgi_app, wsgi_client):
    class Media:
        def on_post(self, request: Request):
            """
            Test multipart/form-data
            """

            files: FileStorage = request.files["file"]
            if not isinstance(files, list):
                files = [files]

            for f in files:
                with open(f.filename, "wb") as fp:
                    f.save(fp)

            return JSONResponse({"success": 1})

    wsgi_app.add_route("/media", Media())
    filename = "falca.png"
    files = {
        "file": ("test_" + filename, open(filename, "rb"), guess_type(filename)[0])
    }
    resp = wsgi_client.post("/media", files=files)
    assert resp.json["success"] == 1
