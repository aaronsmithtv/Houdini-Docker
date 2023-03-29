class APIError(Exception):
    """Raised from the client if the server generated an error while calling
    into the API.
    """
    def __init__(self, http_code, message, response=None):
        super(APIError, self).__init__(message)
        self.http_code = http_code
        self.response = response

    def __str__(self):
        return "%s %s" % (self.http_code, self.args[0])


class AuthorizationError(Exception):
    """
    Raised from the client if the server generated an error while generating
    an access token.
    """
    def __init__(self, http_code, message):
        super(AuthorizationError, self).__init__(message)
        self.http_code = http_code
