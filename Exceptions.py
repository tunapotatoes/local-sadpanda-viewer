#!/usr/bin/env python
from Logger import Logger


class BaseException(Exception, Logger):
    fatal = False

    def __init__(self):
        super(BaseException, self).__init__()
        self.logger.error("%s raised with message %s" %
                          (self.__class__.__name__, self.msg))


class BadCredentialsError(BaseException):
    "Raised for incorrect/missing credentials"

    msg = "Your user id/password hash combination is incorrect."


class UserBannedError(BaseException):
    "Raised when user is banned on SP"

    msg = "You are currently banned on EX."


class InvalidExUrl(BaseException):
    "Raised when user inputs invalid ex url for a gallery"

    msg = "The URL you entered is invalid.\nThe configurations will not be saved."


class InvalidRatingSearch(BaseException):
    "Raised when an incorrect rating function is given to search"

    msg = "The rating function you provided is invalid."  # TODO better wording


class InvalidZip(BaseException):
    bad_perm_msg = "The following zip files have incorrect permissions.\nPlease ensure everyone has write access to them.\n%s"
    bad_file_msg = "The following files failed to open as a valid zip file.\n%s"
    msg = ""

    def __init__(self, invalid_permissions=None, invalid_files=None):
        if invalid_files:
            self.msg += self.bad_file_msg % "\n".join(invalid_files)
        if invalid_permissions:
            self.msg += self.bad_perm_msg % "\n".join(invalid_permissions)
        super(InvalidZip, self).__init__()
