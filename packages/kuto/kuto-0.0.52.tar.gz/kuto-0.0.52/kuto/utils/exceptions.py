class QException(Exception):
    def __init__(self, msg=None, screen=None, stacktrace=None):
        self.msg = msg
        self.screen = screen
        self.stacktrace = stacktrace

    def __str__(self):
        _msg = f"Message: {self.msg}\n"
        if self.screen is not None:
            _msg += f"Screenshot: available via screen\n"
        if self.stacktrace is not None:
            stacktrace = "\n".join(self.stacktrace)
            _msg += f"Stacktrace:\n{stacktrace}"
        return _msg


class ElementTypeError(QException):
    """
    Find Element types Error
    """
    pass


class NoSuchElementException(QException):
    """
    Element could not found
    """
    pass


class TimeoutException(QException):
    """
    Thrown when a command does not complete in enough time.
    """
    pass


class DeviceNotFoundException(QException):
    """
    设备未找到
    """
    pass


class ElementNameEmptyException(QException):
    """
    控件名称为空
    """
    pass


class ScreenFailException(QException):
    """
    截图失败
    """
    pass


class PlatformError(QException):
    """
    平台设置错误
    """


class DriverNotFound(QException):
    """
    driver未传入
    """


class NoSuchDriverType(QException):
    """
    不支持的驱动类型
    """


class PkgIsNull(QException):
    """
    包名为空
    """


class LocMethodEmptyException(QException):
    """
    定位方式为空
    """


class HostIsNull(QException):
    """
    域名为空
    """


class LocMethodNotOne(QException):
    """
    定位方式超过一种
    """


class ConnectInfoIsNull(QException):
    """
    device_id、remote_addr必须有一个不为空
    """


class SibRemoteConnectFail(QException):
    """
    sib远程连接失败
    """


class WDAStartFail(QException):
    """
    wda启动失败
    """

