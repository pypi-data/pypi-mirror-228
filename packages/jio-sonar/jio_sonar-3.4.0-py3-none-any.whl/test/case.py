from builtins import str
import re
import sys
import socket
import time
import types
import unittest
import warnings
import functools
import imp
import weakref
from jio_sonar.marionette_client.errors import KaiOSMarionetteException, SessionNotCreatedException
from jio_sonar.logging import structuredlog
from jio_sonar.device.adbmanager import KaiOSDeviceManagerADB
from future.utils import with_metaclass


class SkipTest(Exception):
    pass


class _ExpectedFailure(Exception):
    def __init__(self, exc_info):
        super(_ExpectedFailure, self).__init__()
        self.exc_info = exc_info


class _UnexpectedSuccess(Exception):
    pass


def skip(reason):
    """
    Unconditionally skip a test.
    """
    def decorator(test_item):
        if not isinstance(test_item, type):
            @functools.wraps(test_item)
            def skip_wrapper(*args, **kwargs):
                raise SkipTest(reason)
            test_item = skip_wrapper

        test_item.__unittest_skip__ = True
        test_item.__unittest_skip_why__ = reason
        return test_item
    return decorator


def expectedFailure(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            raise _ExpectedFailure(sys.exc_info())
        raise _UnexpectedSuccess
    return wrapper


def parameterized(func_suffix, *args, **kwargs):
    """
    A decorator that can generate methods given a base method and some data.

    **func_suffix** is used as a suffix for the new created method and must be
    unique given a base method. if **func_suffix** contains characters that
    are not allowed in normal python function name, these characters will be
    replaced with "_".

    This decorator can be used more than once on a single base method. The class
    must have a metaclass of :class:`MetaParameterized`.

    Example::

      # This example will generate two methods:
      #
      # - MyTestCase.test_it_1
      # - MyTestCase.test_it_2
      #
      class MyTestCase(MarionetteTestCase):
          @parameterized("1", 5, named='name')
          @parameterized("2", 6, named='name2')
          def test_it(self, value, named=None):
              print value, named

    :param func_suffix: will be used as a suffix for the new method
    :param \*args: arguments to pass to the new method
    :param \*\*kwargs: named arguments to pass to the new method
    """
    def wrapped(func):
        if not hasattr(func, 'metaparameters'):
            func.metaparameters = []
        func.metaparameters.append((func_suffix, args, kwargs))
        return func
    return wrapped


def wraps_parameterized(func, func_suffix, args, kwargs):
    def wrapper(self):
        return func(self, *args, **kwargs)
    wrapper.__name__ = func.__name__ + '_' + str(func_suffix)
    wrapper.__doc__ = '[%s] %s' % (func_suffix, func.__doc__)
    return wrapper


class KaiOSMetaParameterized(type):
    """
    A metaclass that allow a class to use decorators like :func:`parameterized`
    to generate new methods.
    """
    RE_ESCAPE_BAD_CHARS = re.compile(r'[\.\(\) -/]')
    def __new__(cls, name, bases, attrs):
        for k, v in list(attrs.items()):
            if callable(v) and hasattr(v, 'metaparameters'):
                for func_suffix, args, kwargs in v.metaparameters:
                    func_suffix = cls.RE_ESCAPE_BAD_CHARS.sub('_', func_suffix)
                    wrapper = wraps_parameterized(v, func_suffix, args, kwargs)
                    if wrapper.__name__ in attrs:
                        raise KeyError("%s is already a defined method on %s" %
                                        (wrapper.__name__, name))
                    attrs[wrapper.__name__] = wrapper
                del attrs[k]

        return type.__new__(cls, name, bases, attrs)


class KaiOSMarionetteTestCase(with_metaclass(KaiOSMetaParameterized, unittest.TestCase)):

    match_re = re.compile(r"test_(.*)\.py$")
    failureException = AssertionError
    pydebugger = None

    def __init__(self, marionette_weakref, methodName='runTest',
                 filepath='', **kwargs):
        unittest.TestCase.__init__(self, methodName)
        self._marionette_weakref = marionette_weakref
        self.marionette = None
        self.methodName = methodName
        self.filepath = filepath
        self.testvars = kwargs.pop('testvars', None)
        self.loglines = []
        self.duration = 0
        self.start_time = 0
        self.expected = kwargs.pop('expected', 'pass')
        self.logger = structuredlog.get_default_logger()
        self._device_manager = None

    def _enter_pm(self):
        if self.pydebugger:
            self.pydebugger.post_mortem(sys.exc_info()[2])

    def _addSkip(self, result, reason):
        addSkip = getattr(result, 'addSkip', None)
        if addSkip is not None:
            addSkip(self, reason)
        else:
            warnings.warn("TestResult has no addSkip method, skips not reported",
                          RuntimeWarning, 2)
            result.addSuccess(self)

    def run(self, result=None):
        # Bug 967566 suggests refactoring run, which would hopefully
        # mean getting rid of this inner function, which only sits
        # here to reduce code duplication:
        def expected_failure(result, exc_info):
            addExpectedFailure = getattr(result, "addExpectedFailure", None)
            if addExpectedFailure is not None:
                addExpectedFailure(self, exc_info)
            else:
                warnings.warn("TestResult has no addExpectedFailure method, "
                              "reporting as passes", RuntimeWarning)
                result.addSuccess(self)

        self.start_time = time.time()
        orig_result = result
        if result is None:
            result = self.defaultTestResult()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()

        result.startTest(self)

        testMethod = getattr(self, self._testMethodName)
        if (getattr(self.__class__, "__unittest_skip__", False)
             or getattr(testMethod, "__unittest_skip__", False)):
            # If the class or method was skipped.
            try:
                skip_why = (getattr(self.__class__, '__unittest_skip_why__', '')
                        or getattr(testMethod, '__unittest_skip_why__', ''))
                self._addSkip(result, skip_why)
            finally:
                result.stopTest(self)
            self.stop_time = time.time()
            return
        try:
            success = False
            try:
                if self.expected == "fail":
                    try:
                        self.setUp()
                    except Exception:
                        raise _ExpectedFailure(sys.exc_info())
                else:
                    self.setUp()
            except SkipTest as e:
                self._addSkip(result, str(e))
            except KeyboardInterrupt:
                raise
            except _ExpectedFailure as e:
                expected_failure(result, e.exc_info)
            except:
                self._enter_pm()
                result.addError(self, sys.exc_info())
            else:
                try:
                    if self.expected == 'fail':
                        try:
                            testMethod()
                        except:
                            raise _ExpectedFailure(sys.exc_info())
                        raise _UnexpectedSuccess
                    else:
                        testMethod()
                except self.failureException:
                    self._enter_pm()
                    result.addFailure(self, sys.exc_info())
                except KeyboardInterrupt:
                    raise
                except _ExpectedFailure as e:
                    expected_failure(result, e.exc_info)
                except _UnexpectedSuccess:
                    addUnexpectedSuccess = getattr(result, 'addUnexpectedSuccess', None)
                    if addUnexpectedSuccess is not None:
                        addUnexpectedSuccess(self)
                    else:
                        warnings.warn("TestResult has no addUnexpectedSuccess method, reporting as failures",
                                      RuntimeWarning)
                        result.addFailure(self, sys.exc_info())
                except SkipTest as e:
                    self._addSkip(result, str(e))
                except:
                    self._enter_pm()
                    result.addError(self, sys.exc_info())
                else:
                    success = True
                try:
                    if self.expected == "fail":
                        try:
                            self.tearDown()
                        except:
                            raise _ExpectedFailure(sys.exc_info())
                    else:
                        self.tearDown()
                except KeyboardInterrupt:
                    raise
                except _ExpectedFailure as e:
                    expected_failure(result, e.exc_info)
                except:
                    self._enter_pm()
                    result.addError(self, sys.exc_info())
                    success = False
            # Here we could handle doCleanups() instead of
            #  calling cleanTest directly
            self.cleanTest()

            if success:
                result.addSuccess(self)
        finally:
            result.stopTest(self)
            if orig_result is None:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()

    @classmethod
    def match(cls, filename):
        """
        Determines if the specified filename should be handled by this
        test class; this is done by looking for a match for the filename
        using cls.match_re.
        """
        if not cls.match_re:
            return False
        m = cls.match_re.match(filename)
        return m is not None

    @classmethod
    def add_tests_to_suite(cls, mod_name, filepath, suite, testloader,
                           marionette, testvars, filter_type, **kwargs):
        # we use filter_type to skip test type defined in decorator
        setattr(cls, 'filter_type', filter_type)
        if mod_name in sys.modules:
            del sys.modules[mod_name]

        test_mod = imp.load_source(mod_name, filepath)

        for name in dir(test_mod):
            obj = getattr(test_mod, name)
            if (isinstance(obj, type) and
                    issubclass(obj, unittest.TestCase)):
                testnames = testloader.getTestCaseNames(obj)
                for testname in testnames:
                    suite.addTest(obj(weakref.ref(marionette),
                                      methodName=testname,
                                      filepath=filepath,
                                      testvars=testvars,
                                      **kwargs))

    @property
    def test_name(self):
        return '%s.py %s.%s' % (self.__class__.__module__,
                                self.__class__.__name__,
                                self._testMethodName)

    def setUp(self):
        # Convert the marionette weakref to an object, just for the
        # duration of the test; this is deleted in tearDown() to prevent
        # a persistent circular reference which in turn would prevent
        # proper garbage collection.
        self.start_time = time.time()
        self.marionette = self._marionette_weakref()
        if self.marionette.session is None:
            self.marionette.start_session()

        if self.marionette.timeout is not None:
            self.marionette.timeouts(self.marionette.TIMEOUT_SEARCH, self.marionette.timeout)
            self.marionette.timeouts(self.marionette.TIMEOUT_SCRIPT, self.marionette.timeout)
            self.marionette.timeouts(self.marionette.TIMEOUT_PAGE, self.marionette.timeout)
        else:
            self.marionette.timeout = 10000
            self.marionette.timeouts(self.marionette.TIMEOUT_SEARCH, 10000)
            self.marionette.timeouts(self.marionette.TIMEOUT_SCRIPT, 20000)
            self.marionette.timeouts(self.marionette.TIMEOUT_PAGE, 20000)

        self.marionette.test_name = self.test_name
        self.marionette.execute_script("log('TEST-START: %s:%s')" %
                                       (self.filepath.replace('\\', '\\\\'), self.methodName))

    def tearDown(self):
        if not self.marionette.check_for_crash():
            try:
                self.marionette.clear_imported_scripts()
                self.marionette.set_context(self.marionette.CONTEXT_CHROME)
                self.marionette.clear_imported_scripts()
                self.marionette.set_context(self.marionette.CONTEXT_CONTENT)
                self.marionette.execute_script("log('TEST-END: %s:%s')" %
                                               (self.filepath.replace('\\', '\\\\'),
                                                self.methodName))
                self.marionette.test_name = None
            except (KaiOSMarionetteException, IOError):
                # We have tried to log the test end when there is no listener
                # object that we can access
                pass

    def cleanTest(self):
        self._deleteSession()

    def _deleteSession(self):
        if hasattr(self, 'start_time'):
            self.duration = time.time() - self.start_time
        if hasattr(self.marionette, 'session'):
            if self.marionette.session is not None:
                try:
                    self.loglines.extend(self.marionette.get_logs())
                except Exception as inst:
                    self.loglines = [['Error getting log: %s' % inst]]
                try:
                    self.marionette.delete_session()
                except (socket.error, KaiOSMarionetteException, IOError):
                    # Gecko has crashed?
                    self.marionette.session = None
                    try:
                        self.marionette.client.close()
                    except socket.error:
                        pass
        self.marionette = None

    @property
    def device_manager(self):
        if not self._device_manager:
            self._device_manager = KaiOSDeviceManagerADB(deviceSerial=self.marionette.device_serial,
                                                    serverHost=self.marionette.adb_host,
                                                    serverPort=self.marionette.adb_port)
        return self._device_manager
