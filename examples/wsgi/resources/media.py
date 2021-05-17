from falca.middleware.files import FileStorage
from falca.request import Request
from falca.resource import Resource
from falca.responses import JsonResponse


class Media(Resource):
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

        return JsonResponse({"success": 1})
