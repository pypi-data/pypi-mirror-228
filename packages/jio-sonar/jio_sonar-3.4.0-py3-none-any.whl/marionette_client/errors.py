# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import traceback

import six


class InstallGeckoError(Exception):
    pass


@six.python_2_unicode_compatible
class KaiOSMarionetteException(Exception):

    """Raised when a generic non-recoverable exception has occured."""

    code = (500,)
    status = "webdriver error"

    def __init__(self, message=None, cause=None, stacktrace=None):
        """Construct new KaiOSMarionetteException instance.

        :param message: An optional exception message.

        :param cause: An optional tuple of three values giving
            information about the root exception cause.  Expected
            tuple values are (type, value, traceback).

        :param stacktrace: Optional string containing a stacktrace
            (typically from a failed JavaScript execution) that will
            be displayed in the exception's string representation.

        """
        self.cause = cause
        self.stacktrace = stacktrace
        self._message = six.text_type(message)

    def __str__(self):
        # pylint: disable=W1645
        msg = self.message
        tb = None

        if self.cause:
            if type(self.cause) is tuple:
                msg += u", caused by {0!r}".format(self.cause[0])
                tb = self.cause[2]
            else:
                msg += u", caused by {}".format(self.cause)

        if self.stacktrace:
            st = u"".join(["\t{}\n".format(x) for x in self.stacktrace.splitlines()])
            msg += u"\nstacktrace:\n{}".format(st)

        if tb:
            msg += u": " + u"".join(traceback.format_tb(tb))

        return six.text_type(msg)

    @property
    def message(self):
        return self._message


class DetachedShadowRootException(KaiOSMarionetteException):
    status = "detached shadow root"


class ElementNotSelectableException(KaiOSMarionetteException):
    status = "element not selectable"


class ElementClickInterceptedException(KaiOSMarionetteException):
    status = "element click intercepted"


class InsecureCertificateException(KaiOSMarionetteException):
    status = "insecure certificate"


class InvalidArgumentException(KaiOSMarionetteException):
    status = "invalid argument"


class InvalidSessionIdException(KaiOSMarionetteException):
    status = "invalid session id"


class TimeoutException(KaiOSMarionetteException):
    code = (21,)
    status = "timeout"


class JavascriptException(KaiOSMarionetteException):
    code = (17,)
    status = "javascript error"


class NoSuchElementException(KaiOSMarionetteException):
    code = (7,)
    status = "no such element"


class NoSuchShadowRootException(KaiOSMarionetteException):
    status = "no such shadow root"


class NoSuchWindowException(KaiOSMarionetteException):
    code = (23,)
    status = "no such window"


class StaleElementException(KaiOSMarionetteException):
    code = (10,)
    status = "stale element reference"


class ScriptTimeoutException(KaiOSMarionetteException):
    code = (28,)
    status = "script timeout"


class ElementNotVisibleException(KaiOSMarionetteException):
    """Deprecated.  Will be removed with the release of Firefox 54."""
    code = (11,)
    status = "element not visible"

    def __init__(
        self,
        message="Element is not currently visible and may not be manipulated",
        stacktrace=None,
        cause=None,
    ):
        super(ElementNotVisibleException, self).__init__(
            message, cause=cause, stacktrace=stacktrace
        )


class ElementNotAccessibleException(KaiOSMarionetteException):
    code = (56,)
    status = "element not accessible"


class ElementNotInteractableException(KaiOSMarionetteException):
    status = "element not interactable"


class NoSuchFrameException(KaiOSMarionetteException):
    code = (8,)
    status = "no such frame"


class InvalidElementStateException(KaiOSMarionetteException):
    code = (12,)
    status = "invalid element state"


class NoAlertPresentException(KaiOSMarionetteException):
    code = (27,)
    status = "no such alert"


class InvalidCookieDomainException(KaiOSMarionetteException):
    code = (24,)
    status = "invalid cookie domain"


class UnableToSetCookieException(KaiOSMarionetteException):
    code = (25,)
    status = "unable to set cookie"


class InvalidElementCoordinates(KaiOSMarionetteException):
    code = (29,)
    status = "invalid element coordinates"


class InvalidSelectorException(KaiOSMarionetteException):
    code = (32, 51, 52)
    status = "invalid selector"


class MoveTargetOutOfBoundsException(KaiOSMarionetteException):
    code = (34,)
    status = "move target out of bounds"


class SessionNotCreatedException(KaiOSMarionetteException):
    code = (33, 71)
    status = "session not created"


class UnexpectedAlertOpen(KaiOSMarionetteException):
    code = (26,)
    status = "unexpected alert open"


class UnknownCommandException(KaiOSMarionetteException):
    code = (9,)
    status = "unknown command"


class UnknownException(KaiOSMarionetteException):
    code = (13,)
    status = "unknown error"


class UnsupportedOperationException(KaiOSMarionetteException):
    code = (405,)
    status = "unsupported operation"


class UnresponsiveInstanceException(Exception):
    pass


es_ = [
    e
    for e in locals().values()
    if type(e) == type and issubclass(e, KaiOSMarionetteException)
]
by_string = {e.status: e for e in es_}


def lookup(identifier):
    """Finds error exception class by associated Selenium JSON wire
    protocol number code, or W3C WebDriver protocol string.

    """
    return by_string.get(identifier, KaiOSMarionetteException)
