from falca.middleware.files import FileStorage
from falca.resource import Resource


class Media(Resource):
    def on_post(self):
        files: FileStorage = self.request.files["file"]
        if not isinstance(files, list):
            files = [files]

        for f in files:
            with open(f.filename, "wb") as fp:
                f.save(fp)

        self.json({"success": 1})
