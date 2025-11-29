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
    error_code = 100001
    message = "Unexpected error"


class InvalidParameter(APIException):
    error_code = 100002
    message = "Invalid parameter"


class ExceptUsernameExist(APIException):
    http_code = 200
    error_code = 100003
    message = "用户名或邮箱已存在，请使用其他用户名或邮箱"


class ExceptEmailExist(APIException):
    http_code = 200
    error_code = 100004
    message = "用户名或邮箱已存在，请使用其他用户名或邮箱"


class ExceptEmailRdsCodeNotExist(APIException):
    http_code = 200
    error_code = 100005
    message = "验证码不存在或错误"


class ExceptEmailNotExist(APIException):
    http_code = 200
    error_code = 100005
    message = "账号密码错误"


class ExceptPwdNotMatch(APIException):
    http_code = 200
    error_code = 100006
    message = "账号密码错误"


class ExceptJwtInvalidToken(APIException):
    http_code = 200
    error_code = 100007
    message = "账号密码错误"


class ExceptJwtTokenExprited(APIException):
    http_code = 200
    error_code = 100008
    message = "登陆过期，请重新登录"


# 不是管理员
class ExceptIsNotStuff(APIException):
    http_code = 200
    error_code = 100009
    message = "权限不足"


# 不是超级管理员
class ExceptIsNotSuperuser(APIException):
    http_code = 200
    error_code = 100010
    message = "权限不足"


class ExceptFeedBackTypeExist(APIException):
    http_code = 200
    error_code = 100011
    message = "反馈类型已经存在请勿重复创建"


class ExceptFeedBackTypeNotExist(APIException):
    http_code = 200
    error_code = 100011
    message = "数据不存在"


class ExceptFeedRecordTypeNotExist(APIException):
    http_code = 200
    error_code = 100012
    message = "数据不存在"
