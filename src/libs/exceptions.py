# -*- coding:utf-8 -*-
INVALID_PARAMETER = 40002
CABINET_NOT_FOUND = 40401
UNEXPECTED_ERROR = 50000


class APIException(Exception):
    http_code = 400  # http 状体码
    error_code = 40000  # 业务状态码
    message = "APIException occured, bad request"  # 返回给前端的消息

    def __init__(self, http_code=None, error_code=None, message=None):
        super().__init__()
        self.http_code = http_code or self.http_code
        self.error_code = error_code or self.error_code
        self.message = message or self.message

    def __str__(self):
        return f"error_code: {self.error_code}, message: {self.message}"

    def to_dict(self):
        return {
            "http_code": self.http_code,
            "error_code": self.error_code,
            "message": self.message,
        }

    __repr__ = __str__


class Unauthorized(APIException):
    http_code = 401


class Forbidden(APIException):
    http_code = 403


class NotFound(APIException):
    http_code = 404


class InternalError(APIException):
    http_code = 500


class ServiceUnavailable(APIException):
    http_code = 503


class UnexpectedError(InternalError):
    error_code = UNEXPECTED_ERROR
    message = "Unexpected error"


class InvalidParameter(APIException):
    error_code = INVALID_PARAMETER
    message = "Invalid parameter"

