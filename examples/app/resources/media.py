from falca.middleware.files import FileStorage
from falca.resource import Resource


class Media(Resource):
    def on_post(self):
        file: FileStorage = self.request.files["file"]
        with open("uploaded_image.jpeg", "wb") as fp:
            file.save(fp)

        self.json({"success": 1})
