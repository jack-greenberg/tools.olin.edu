class AppException(Exception):
    def __init__(self, message, code=500, **kwargs):
        Exception.__init__(self)
        self.message = message
        self.code = code
        self.kwargs = kwargs

    def to_dict(self):
        rv = dict(self.kwargs or ())
        rv["message"] = self.message
        return rv
