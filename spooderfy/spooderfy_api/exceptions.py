class ApiException(Exception):
    """ The base exception of all api errors"""


class HttpException(ApiException):
    """ Raised when the status is not a 2xx code"""
