from falca.middleware.files import FileStorage
from falca.request import ASGIRequest
from falca.responses import JSONResponse


class Media:
    async def on_post(self, request: ASGIRequest):
        files: FileStorage = request.files["file"]
        if not isinstance(files, list):
            files = [files]

        for f in files:
            with open(f.filename, "wb") as fp:
                f.save(fp)

        return JSONResponse({"success": 1})
