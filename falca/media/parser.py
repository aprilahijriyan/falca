from webargs.falconparser import FalconParser as Parser


class FalconParser(Parser):
    def load_files(self, req, schema):
        return self._makeproxy(req.files, schema)


parser = FalconParser()
use_args = parser.use_args
use_kwargs = parser.use_kwargs
