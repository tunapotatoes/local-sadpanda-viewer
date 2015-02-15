#!/usr/bin/env python
from Logger import Logger


class BaseException(Exception, Logger):
    def __init__(self, msg=None):
        super(BaseException, self).__init__()
        assert self.__class.__name__!= "BaseException"  # Ensure this doesn't get raised
        self.msg = msg
        self.logger.warning("%s raised with message %s" %
                            (self.__class__.__name__, self.msg))


class BadCredentialsError(BaseException):
    "Raised for incorrect/missing credentials"


class UserBannedError(BaseException):
    "Raised when user is banned on SP"
