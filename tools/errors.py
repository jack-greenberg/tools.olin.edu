class AppException(Exception):
    def __init__(self, message, code=500, **kwargs):
        Exception.__init__(self)
        self.message = message
        self.code = code
        self.kwargs = kwargs

    def to_dict(self):
        rv = dict(self.kwargs or ())
        rv["message"] = self.message
        rv["code"] = self.code
        return rv


class AuthException(AppException):
    def __init__(self, message, code=401, **kwargs):
        AppException.__init__(self, message, code=code, **kwargs)


class LoginRequired(AppException):
    def __init__(self, message, code=401, **kwargs):
        AppException.__init__(self, message, code=code, **kwargs)
