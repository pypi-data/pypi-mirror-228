import os
import re
import time

import unittest
import traceback
import sys
from jio_sonar.device.adbmanager import KaiOSDeviceManagerADB


class KaiOSMarionetteTest(object):
    """ Stores test result data """

    FAIL_RESULTS = [
        'UNEXPECTED-PASS',
        'UNEXPECTED-FAIL',
        'ERROR',
    ]
    COMPUTED_RESULTS = FAIL_RESULTS + [
        'PASS',
        'KNOWN-FAIL',
        'SKIPPED',
    ]
    POSSIBLE_RESULTS = [
        'PASS',
        'FAIL',
        'SKIP',
        'ERROR',
    ]

    def __init__(self, name, test_class='', time_start=None, context=None,
                 result_expected='PASS'):
        """
        Create a TestResult instance.
        :param name: name of the test that is running
        :param test_class: the class that the test belongs to
        :param time_start: timestamp (seconds since UNIX epoch) of when the test started
                           running; if not provided, defaults to the current time
                           ! Provide 0 if you only have the duration
        :param context: TestContext instance; can be None
        :param result_expected: string representing the expected outcome of the test
        :return:
        """
        msg = "Result '%s' not in possible results: %s" %\
              (result_expected, ', '.join(self.POSSIBLE_RESULTS))
        assert isinstance(name, str), "name has to be a string"
        assert result_expected in self.POSSIBLE_RESULTS, msg

        self.name = name
        self.test_class = test_class
        self.context = context
        self.time_start = time_start if time_start is not None else time.time()
        self.time_end = None
        self._result_expected = result_expected
        self._result_actual = None
        self.result = None
        self.filename = None
        self.description = None
        self.output = []
        self.reason = None

    @property
    def test_name(self):
        if self.test_class is not None:
            return '%s.py %s.%s' % (self.test_class.split('.')[0],
                                    self.test_class,
                                    self.name)
        else:
            return self.name

    def __str__(self):
        return '%s | %s (%s) | %s' % (self.result or 'PENDING',
                                      self.name, self.test_class, self.reason)

    def __repr__(self):
        return '<%s>' % self.__str__()

    def calculate_result(self, expected, actual):
        if actual == 'ERROR':
            return 'ERROR'
        if actual == 'SKIP':
            return 'SKIPPED'

        if expected == 'PASS':
            if actual == 'PASS':
                return 'PASS'
            if actual == 'FAIL':
                return 'UNEXPECTED-FAIL'

        if expected == 'FAIL':
            if actual == 'PASS':
                return 'UNEXPECTED-PASS'
            if actual == 'FAIL':
                return 'KNOWN-FAIL'

        return 'ERROR'

    def infer_results(self, computed_result):
        assert computed_result in self.COMPUTED_RESULTS
        if computed_result == 'UNEXPECTED-PASS':
            expected = 'FAIL'
            actual = 'PASS'
        elif computed_result == 'UNEXPECTED-FAIL':
            expected = 'PASS'
            actual = 'FAIL'
        elif computed_result == 'KNOWN-FAIL':
            expected = actual = 'FAIL'
        elif computed_result == 'SKIPPED':
            expected = actual = 'SKIP'
        else:
            return
        self._result_expected = expected
        self._result_actual = actual

    def finish(self, result, time_end=None, output=None, reason=None):
        """ Marks the test as finished, storing its end time and status
        ! Provide the duration as time_end if you only have that. """

        if result in self.POSSIBLE_RESULTS:
            self._result_actual = result
            self.result = self.calculate_result(self._result_expected,
                                                self._result_actual)
        elif result in self.COMPUTED_RESULTS:
            self.infer_results(result)
            self.result = result
        else:
            valid = self.POSSIBLE_RESULTS + self.COMPUTED_RESULTS
            msg = "Result '%s' not valid. Need one of: %s" %\
                  (result, ', '.join(valid))
            raise ValueError(msg)

        # use lists instead of multiline strings
        if isinstance(output, str):
            output = output.splitlines()

        self.time_end = time_end if time_end is not None else time.time()
        self.output = output or self.output
        self.reason = reason

    @property
    def finished(self):
        """ Boolean saying if the test is finished or not """
        return self.result is not None

    @property
    def duration(self):
        """ Returns the time it took for the test to finish. If the test is
        not finished, returns the elapsed time so far """
        if self.result is not None:
            return self.time_end - self.time_start
        else:
            # returns the elapsed time
            return time.time() - self.time_start


class KaiOSMarionetteTestResult(unittest.TextTestResult, list):

    resultClass = KaiOSMarionetteTest

    def __init__(self, *args, **kwargs):
        list.__init__(self)
        self.marionette = kwargs.pop('marionette')
        self.passed = 0
        self.testsRun = 0
        self.result_modifiers = [] # used by mixins to modify the result
        pid = kwargs.pop('b2g_pid')
        if pid:
            if KaiOSB2GTestResultMixin not in self.__class__.__bases__:
                bases = [b for b in self.__class__.__bases__]
                bases.append(KaiOSB2GTestResultMixin)
                self.__class__.__bases__ = tuple(bases)
            KaiOSB2GTestResultMixin.__init__(self, b2g_pid=pid)
        self.logger = kwargs.pop('logger')
        self.test_list = kwargs.pop("test_list", [])
        self.result_callbacks = kwargs.pop('result_callbacks', [])
        unittest.TextTestResult.__init__(self, *args, **kwargs)

    def call_callbacks(self, test, status):
        debug_info = {}
        for callback in self.result_callbacks:
            info = callback(test, status)
            if info is not None:
                debug_info.update(info)
        return debug_info

    def startTestRun(self):
        # This would be an opportunity to call the logger's suite_start action,
        # however some users may use multiple suites, and per the structured
        # logging protocol, this action should only be called once.
        pass

    def startTest(self, test):
        self.testsRun += 1
        self.logger.test_start(test.id())

    def stopTestRun(self):
        # This would be an opportunity to call the logger's suite_end action,
        # however some users may use multiple suites, and per the structured
        # logging protocol, this action should only be called once.
        pass

    def _extract_err_message(self, err):
        # Format an exception message in the style of unittest's _exc_info_to_string
        # while maintaining a division between a traceback and a message.
        exc_ty, val, _ = err
        exc_msg = "".join(traceback.format_exception_only(exc_ty, val))
        if self.buffer:
            output_msg = "\n".join([sys.stdout.getvalue(), sys.stderr.getvalue()])
            return "".join([exc_msg, output_msg])
        return exc_msg.rstrip()

    def _extract_stacktrace(self, err, test):
        # Format an exception stack in the style of unittest's _exc_info_to_string
        # while maintaining a division between a traceback and a message.
        # This is mostly borrowed from unittest.result._exc_info_to_string.

        exctype, value, tb = err
        while tb and self._is_relevant_tb_level(tb):
            tb = tb.tb_next
        # Header usually included by print_exception
        lines = ["Traceback (most recent call last):\n"]
        if exctype is test.failureException:
            length = self._count_relevant_tb_levels(tb)
            lines += traceback.format_tb(tb, length)
        else:
            lines += traceback.format_tb(tb)
        return "".join(lines)

    def _get_class_method_name(self, test):
        return {
            'class_name': self.get_test_class_name(test),
            'method_name': self.get_test_method_name(test)
        }

    @property
    def skipped(self):
        return [t for t in self if t.result == 'SKIPPED']

    @skipped.setter
    def skipped(self, value):
        pass

    @property
    def expectedFailures(self):
        return [t for t in self if t.result == 'KNOWN-FAIL']

    @expectedFailures.setter
    def expectedFailures(self, value):
        pass

    @property
    def unexpectedSuccesses(self):
        return [t for t in self if t.result == 'UNEXPECTED-PASS']

    @unexpectedSuccesses.setter
    def unexpectedSuccesses(self, value):
        pass

    @property
    def tests_passed(self):
        return [t for t in self if t.result == 'PASS']

    @property
    def errors(self):
        return [t for t in self if t.result == 'ERROR']

    @errors.setter
    def errors(self, value):
        pass

    @property
    def failures(self):
        return [t for t in self if t.result == 'UNEXPECTED-FAIL']

    @failures.setter
    def failures(self, value):
        pass

    @property
    def duration(self):
        if self.stop_time:
            return self.stop_time - self.start_time
        else:
            return 0

    def add_test_result(self, test, result_expected='PASS',
                        result_actual='PASS', output='', context=None, **kwargs):
        def get_class(test):
            return test.__class__.__module__ + '.' + test.__class__.__name__

        name = str(test).split()[0]
        test_class = get_class(test)
        if hasattr(test, 'jsFile'):
            name = os.path.basename(test.jsFile)
            test_class = None

        t = self.resultClass(name=name, test_class=test_class,
                       time_start=test.start_time, result_expected=result_expected,
                       context=context, **kwargs)
        # call any registered result modifiers
        for modifier in self.result_modifiers:
            result_expected, result_actual, output, context = modifier(t, result_expected, result_actual, output, context)
        t.finish(result_actual,
                 time_end=time.time() if test.start_time else 0,
                 reason=relevant_line(output),
                 output=output)
        self.append(t)

    def _addNegativeResult(self, test, actual_info, log_info, expected, err=None):
        if err:
            self.add_test_result(test, output=self._exc_info_to_string(err, test), result_actual=actual_info)
            self.errors.append((test, self._exc_info_to_string(err, test)))
            extra = self.call_callbacks(test, actual_info)
            extra.update(self._get_class_method_name(test))
            self.logger.test_end(test.id(),
                                 log_info,
                                 message=self._extract_err_message(err),
                                 expected=expected,
                                 stack=self._extract_stacktrace(err, test),
                                 extra=extra)
        else:
            self.add_test_result(test, result_actual=actual_info)
            extra = self.call_callbacks(test, actual_info)
            extra.update(self._get_class_method_name(test))
            self.logger.test_end(test.id(),
                                 log_info,
                                 expected=expected,
                                 extra=extra)

    def _addPositiveResult(self, test, actual_info, log_info, expected):
        self.add_test_result(test, result_actual=actual_info)
        extra = self._get_class_method_name(test)
        self.logger.test_end(test.id(),
                             log_info,
                             expected=expected,
                             extra=extra)

    def addError(self, test, err):
        self._addNegativeResult(test=test, actual_info="ERROR", log_info="ERROR", expected="PASS", err=err)

    def addFailure(self, test, err):
        self._addNegativeResult(test=test, actual_info="UNEXPECTED-FAIL", log_info="FAIL", expected="PASS", err=err)

    def addSuccess(self, test):
        self.passed += 1
        self._addPositiveResult(test=test, actual_info="PASS", log_info="PASS", expected="PASS")

    def addExpectedFailure(self, test, err):
        """Called when an expected failure/error occured."""
        self._addNegativeResult(test=test, actual_info="KNOWN-FAIL", log_info="FAIL", expected="FAIL", err=err)

    def addUnexpectedSuccess(self, test):
        """Called when a test was expected to fail, but succeed."""
        self._addNegativeResult(test=test, actual_info="UNEXPECTED-PASS", log_info="PASS", expected="FAIL")

    def addSkip(self, test, reason):
        self.add_test_result(test, output=reason, result_actual='SKIPPED')
        extra = self.call_callbacks(test, "SKIP")
        extra.update(self._get_class_method_name(test))
        self.logger.test_end(test.id(),
                             "SKIP",
                             message=reason,
                             expected="PASS",
                             extra=extra)

    def getInfo(self, test):
        return test.test_name

    def getDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return '\n'.join((str(test), doc_first_line))
        else:
            desc = str(test)
            if hasattr(test, 'jsFile'):
                desc = "%s, %s" % (test.jsFile, desc)
            return desc

    def printLogs(self, test):
        for testcase in test._tests:
            if hasattr(testcase, 'loglines') and testcase.loglines:
                # Don't dump loglines to the console if they only contain
                # TEST-START and TEST-END.
                skip_log = True
                for line in testcase.loglines:
                    str_line = ' '.join(line)
                    if not 'TEST-END' in str_line and not 'TEST-START' in str_line:
                        skip_log = False
                        break
                if skip_log:
                    return
                self.logger.info('START LOG:')
                for line in testcase.loglines:
                    self.logger.info(' '.join(line).encode('ascii', 'replace'))
                self.logger.info('END LOG:')

    def stopTest(self, *args, **kwargs):
        unittest._TextTestResult.stopTest(self, *args, **kwargs)
        if self.marionette.check_for_crash():
            # this tells unittest.TestSuite not to continue running tests
            self.shouldStop = True

    @staticmethod
    def get_test_class_name(test):
        return "%s.%s" % (test.__class__.__module__,
                          test.__class__.__name__)

    @staticmethod
    def get_test_method_name(test):
        return test._testMethodName


class KaiOSB2GTestResultMixin(object):

    def __init__(self, *args, **kwargs):
        self.result_modifiers.append(self.b2g_output_modifier)
        self.b2g_pid = kwargs.pop('b2g_pid')

    def _diagnose_socket(self):
        # This function will check if b2g is running and report any recent errors. This is
        # used in automation since a plain timeout error doesn't tell you
        # much information about what actually is going on

        extra_output = None
        dm_type = os.environ.get('DM_TRANS', 'adb')
        if dm_type == 'adb':
            device_manager = get_dm(self.marionette)
            pid = get_b2g_pid(device_manager)
            if pid:
                # find recent errors
                message = ""
                error_re = re.compile(r"""[\s\S]*(exception|error)[\s\S]*""",
                                      flags=re.IGNORECASE)
                logcat = device_manager.getLogcat()
                # Due to Bug 1050211
                if len(logcat) == 1:
                    logcat = logcat[0].splitlines()
                latest = []
                iters = len(logcat) - 1
                # reading from the latest line
                while len(latest) < 5 and iters >= 0:
                    line = logcat[iters]
                    error_log_line = error_re.match(line)
                    if error_log_line is not None:
                        latest.append(line)
                    iters -= 1
                message += "\nMost recent errors/exceptions are:\n"
                for line in reversed(latest):
                    message += "%s" % line
                b2g_status = ""
                if pid != self.b2g_pid:
                    b2g_status = "The B2G process has restarted after crashing during  the tests so "
                else:
                    b2g_status = "B2G is still running but "
                extra_output = ("%s\n%sMarionette can't respond due to either a Gecko, Gaia or Marionette error. "
                                "Above, the 5 most recent errors are listed. "
                                "Check logcat for all errors if these errors are not the cause "
                                "of the failure." % (message, b2g_status))
            else:
                extra_output = "B2G process has died"
        return extra_output

    def b2g_output_modifier(self, test, result_expected, result_actual, output, context):
        # output is the actual string output from the test, so we have to do string comparison
        if "IOError" in output or "Broken pipe" in output or "Connection timed out" in output:
            extra_output = self._diagnose_socket()
            if extra_output:
                self.logger.error(extra_output)
                output += extra_output

        return result_expected, result_actual, output, context


# used to get exceptions/errors from tracebacks
def relevant_line(s):
    KEYWORDS = ('Error:', 'Exception:', 'error:', 'exception:')
    lines = s.splitlines()
    for line in lines:
        for keyword in KEYWORDS:
            if keyword in line:
                return line
    return 'N/A'


def get_b2g_pid(dm):
    b2g_output = dm.shellCheckOutput(['b2g-ps']).split('\n')
    print("b2goutput", b2g_output)
    first_line = b2g_output[0].split()
    app_index = first_line.index('APPLICATION')
    pid_index = first_line.index('PID')
    for line in b2g_output:
        split_line = line.split()
        if split_line[app_index] == 'b2g':
            return split_line[pid_index]


def get_dm(marionette=None, **kwargs):
    dm_type = os.environ.get('DM_TRANS', 'adb')
    if dm_type == 'adb':
        return KaiOSDeviceManagerADB(deviceSerial=marionette.device_serial,
                                serverHost=marionette.adb_host,
                                serverPort=marionette.adb_port,
                                **kwargs)
    else:
        raise Exception('Unknown device manager type: %s' % dm_type)
