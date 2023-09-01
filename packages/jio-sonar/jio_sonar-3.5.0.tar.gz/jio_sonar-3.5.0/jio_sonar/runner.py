from future.utils import raise_
from builtins import object
import json
import random
import sys
import socket
import unittest
import traceback
import time
import os
from jio_sonar.marionette_client import Marionette, FixtureServer
from jio_sonar.marionette_client.errors import SessionNotCreatedException
from jio_sonar.gaia_arguments import GaiaTestArguments
from jio_sonar.test.results import KaiOSMarionetteTestResult, get_b2g_pid, get_dm
from jio_sonar.logging import structuredlog
from jio_sonar.device import version
from manifestparser import TestManifest
from manifestparser.filters import tags


class KaiOSMarionetteTextTestRunner(unittest.TextTestRunner):

    resultclass = KaiOSMarionetteTestResult

    def __init__(self, dm, dm_type, **kwargs):
        self.marionette = kwargs.pop('marionette')
        self.capabilities = kwargs.pop('capabilities')
        self.logger = kwargs.pop("logger")
        self.test_list = kwargs.pop("test_list", [])
        self.result_callbacks = kwargs.pop("result_callbacks", [])
        self.dm_type = dm_type
        self.b2g_pid = get_b2g_pid(dm)
        unittest.TextTestRunner.__init__(self, **kwargs)

    def _makeResult(self):
        return self.resultclass(self.stream,
                                self.descriptions,
                                self.verbosity,
                                marionette=self.marionette,
                                b2g_pid=self.b2g_pid,
                                logger=self.logger,
                                result_callbacks=self.result_callbacks)

    def run(self, test):
        result = self._makeResult()
        result.failfast = self.failfast
        result.buffer = self.buffer
        startTime = time.time()
        startTestRun = getattr(result, 'startTestRun', None)
        if startTestRun is not None:
            startTestRun()
        try:
            test(result)
        finally:
            stopTestRun = getattr(result, 'stopTestRun', None)
            if stopTestRun is not None:
                stopTestRun()
        stopTime = time.time()
        if hasattr(result, 'time_taken'):
            result.time_taken = stopTime - startTime

        result.printLogs(test)
        return result


class KaiOSMarionetteTestRunner(object):

    textrunnerclass = KaiOSMarionetteTextTestRunner
    driverclass = Marionette

    def __init__(self, address=None, logger=None, repeat=0, testvars=None, type=None,
                 device_serial=None, timeout=None, shuffle=False, shuffle_seed=random.randint(0, sys.maxsize),
                 server_root=None, result_callbacks=None,
                 test_tags=None, socket_timeout=GaiaTestArguments.socket_timeout_default,
                 filter_type=None, tolerance_level=1, **kwargs):
        self.address = address
        self.logger = logger
        self.httpd = None
        self.marionette = None
        self.repeat = repeat
        self.test_kwargs = kwargs
        self.type = type
        self.filter_type = filter_type
        self.tolerance_level = tolerance_level
        self.device_serial = device_serial
        self.timeout = timeout
        self.socket_timeout = socket_timeout
        self._device = None
        self._capabilities = None
        self._appName = None
        self.shuffle = shuffle
        self.shuffle_seed = shuffle_seed
        self.server_root = server_root
        self.mixin_run_tests = []
        self.manifest_skipped_tests = []
        self.tests = []
        self.result_callbacks = result_callbacks if result_callbacks is not None else []
        self.test_tags = test_tags
        self.workspace = None
        self.sources = None

        if not self.marionette:
            self.start_marionette()
            self.marionette.start_session()
            self._capabilities = self.capabilities

        self.marionette.tolerance_level = self.tolerance_level
        self.dm = get_dm(self.marionette)
        self.dm_type = os.environ.get('DM_TRANS', 'adb')

        def gather_debug(test, status):
            rv = {}
            marionette = test._marionette_weakref()

            # In the event we're gathering debug without starting a session, skip marionette commands
            if marionette.session is not None:
                try:
                    # with marionette.using_context(marionette.CONTEXT_CHROME):
                    #     rv['screenshot'] = marionette.screenshot()
                    print("trying screenshot")
                except Exception:
                    logger = structuredlog.get_default_logger()
                    logger.warning('Failed to gather test failure debug.', exc_info=True)
            return rv

        self.result_callbacks.append(gather_debug)

        def update(d, u):
            """ Update a dictionary that may contain nested dictionaries. """
            for k, v in u.items():
                o = d.get(k, {})
                if isinstance(v, dict) and isinstance(o, dict):
                    d[k] = update(d.get(k, {}), v)
                else:
                    d[k] = u[k]
            return d

        self.testvars = {}
        if testvars is not None:
            for path in list(testvars):
                if not os.path.exists(path):
                    raise IOError('--testvars file %s does not exist' % path)
                try:
                    with open(path) as f:
                        self.testvars = update(self.testvars,
                                               json.loads(f.read()))
                except ValueError as e:
                    raise Exception("JSON file (%s) is not properly "
                                    "formatted: %s" % (os.path.abspath(path),
                                                       e.message))

        # set up test handlers
        self.test_handlers = []
        self.reset_test_stats()
        self.results = []

    @property
    def capabilities(self):
        if self._capabilities:
            return self._capabilities
        if not self._capabilities and self.marionette.session_capabilities:
            self._capabilities = self.marionette.session_capabilities
        elif not self._capabilities and not self.marionette.session_capabilities:
            self.marionette.start_session()
            self._capabilities = self.marionette.session_capabilities
        return self._capabilities

    @property
    def device(self):
        if self._device:
            return self._device

        self._device = self.capabilities.get('device')
        return self._device

    @property
    def appName(self):
        if self._appName:
            return self._appName

        self._appName = self.capabilities.get('browserName')
        return self._appName

    def reset_test_stats(self):
        self.passed = 0
        self.failed = 0
        self.unexpected_successes = 0
        self.todo = 0
        self.skipped = 0
        self.failures = []

    def _build_kwargs(self):
        kwargs = {
            'device_serial': self.device_serial,
            'timeout': self.timeout,
            'socket_timeout': self.socket_timeout,
        }

        if self.address:
            host, port = self.address.split(':')
            kwargs.update({
                'host': host,
                'port': int(port),
            })
            try:
                #establish a socket connection so we can vertify the data come back
                connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                connection.connect((host,int(port)))
                connection.close()
            except Exception as e:
                raise Exception("Connection attempt to %s:%s failed with error: %s" %(host,port,e))
        return kwargs

    def start_marionette(self):
        self.marionette = self.driverclass(**self._build_kwargs())

    def run_test_set(self, tests):
        if self.shuffle:
            random.seed(self.shuffle_seed)
            random.shuffle(tests)

        for test in tests:
            self.run_test(test['filepath'], test['expected'])
            if self.marionette.check_for_crash():
                break

    def run_test_sets(self):
        if len(self.tests) < 1:
            raise Exception('There are no tests to run.')

        self.run_test_set(self.tests)

    def run_test(self, filepath, expected):

        testloader = unittest.TestLoader()
        suite = unittest.TestSuite()
        self.test_kwargs['expected'] = expected
        mod_name = os.path.splitext(os.path.split(filepath)[-1])[0]
        for handler in self.test_handlers:
            if handler.match(os.path.basename(filepath)):
                # add type from input arguments for filter
                handler.add_tests_to_suite(mod_name,
                                           filepath,
                                           suite,
                                           testloader,
                                           self.marionette,
                                           self.testvars,
                                           self.filter_type,
                                           **self.test_kwargs)
                break

        if suite.countTestCases():
            runner = self.textrunnerclass(dm=self.dm,
                                          dm_type=self.dm_type,
                                          logger=self.logger,
                                          marionette=self.marionette,
                                          capabilities=self.capabilities,
                                          result_callbacks=self.result_callbacks)

            results = runner.run(suite)
            self.results.append(results)

            self.failed += len(results.failures) + len(results.errors)
            if hasattr(results, 'skipped'):
                self.skipped += len(results.skipped)
                self.todo += len(results.skipped)
            self.passed += results.passed
            for failure in results.failures + results.errors:
                self.failures.append((results.getInfo(failure), failure.output, 'TEST-UNEXPECTED-FAIL'))
            if hasattr(results, 'unexpectedSuccesses'):
                self.failed += len(results.unexpectedSuccesses)
                self.unexpected_successes += len(results.unexpectedSuccesses)
                for failure in results.unexpectedSuccesses:
                    self.failures.append((results.getInfo(failure), failure.output, 'TEST-UNEXPECTED-PASS'))
            if hasattr(results, 'expectedFailures'):
                self.todo += len(results.expectedFailures)

            self.mixin_run_tests = []
            for result in self.results:
                result.result_modifiers = []

    def run_tests(self, tests):
        self.reset_test_stats()
        self.start_time = time.time()

        need_external_ip = True
        if self._capabilities['platformName'] == "desktop":
            need_external_ip = False

        # Gaia sets server_root and that means we shouldn't spin up our own httpd
        if not self.httpd:
            if self.server_root is None or os.path.isdir(self.server_root):
                self.logger.info("starting httpd")
                self.start_httpd(need_external_ip)
                self.marionette.baseurl = self.httpd.get_url()
                self.logger.info("running httpd on %s" % self.marionette.baseurl)
            else:
                self.marionette.baseurl = self.server_root
                self.logger.info("using remote content from %s" % self.marionette.baseurl)

        device_info = None
        if self.capabilities['platformName'] != 'desktop':
            device_info = self.dm.getInfo()
            androidVersion = self.dm.shellCheckOutput(['getprop', 'ro.build.version.sdk'])
            self.logger.info(
                "Android sdk version '%s'; will use this to filter manifests" % androidVersion)

        for test in tests:
            self.add_test(test)

        # ensure we have only tests files with names starting with 'test_'
        invalid_tests = \
            [t['filepath'] for t in self.tests
             if not os.path.basename(t['filepath']).startswith('test_')]
        if invalid_tests:
            raise Exception("Tests file names must starts with 'test_'."
                            " Invalid test names:\n  %s"
                            % '\n  '.join(invalid_tests))

        version_info = version.get_version(sources=self.sources,
                                           dm=self.dm,
                                           device_serial=self.device_serial,
                                           adb_host=self.marionette.adb_host,
                                           adb_port=self.marionette.adb_port)

        self.logger.suite_start(self.tests, version_info=version_info, device_info=device_info)

        for test in self.manifest_skipped_tests:
            name = os.path.basename(test['path'])
            self.logger.test_start(name)
            self.logger.test_end(name,
                                 'SKIP',
                                 message=test['disabled'])
            self.todo += 1

        interrupted = None
        try:
            counter = self.repeat
            while counter >=0:
                round = self.repeat - counter
                if round > 0:
                    self.logger.info('\nREPEAT %d\n-------' % round)
                self.run_test_sets()
                counter -= 1
        except KeyboardInterrupt:
            # in case of KeyboardInterrupt during the test execution
            # we want to display current test results.
            # so we keep the exception to raise it later.
            interrupted = sys.exc_info()
        try:
            self._print_summary(tests)
        except:
            # raise only the exception if we were not interrupted
            if not interrupted:
                raise
        finally:
            # reraise previous interruption now
            if interrupted:
                raise_(interrupted[0], interrupted[1], interrupted[2])

    def _print_summary(self, tests):
        self.logger.info('\nSUMMARY\n-------')
        self.logger.info('passed: %d' % self.passed)
        if self.unexpected_successes == 0:
            self.logger.info('failed: %d' % self.failed)
        else:
            self.logger.info('failed: %d (unexpected sucesses: %d)' % (self.failed, self.unexpected_successes))
        if self.skipped == 0:
            self.logger.info('todo: %d' % self.todo)
        else:
            self.logger.info('todo: %d (skipped: %d)' % (self.todo, self.skipped))

        if self.failed > 0:
            self.logger.info('\nFAILED TESTS\n-------')
            for failed_test in self.failures:
                self.logger.info('%s' % failed_test[0])

        try:
            self.marionette.check_for_crash()
        except:
            traceback.print_exc()

        self.end_time = time.time()
        self.elapsedtime = self.end_time - self.start_time

        self.marionette.cleanup()

        for run_tests in self.mixin_run_tests:
            run_tests(tests)
        if self.shuffle:
            self.logger.info("Using seed where seed is:%d" % self.shuffle_seed)

        self.logger.suite_end()

    def start_httpd(self, need_external_ip):
        self.httpd = self.create_httpd(need_external_ip)

    def create_httpd(self, need_external_ip):
        host = "127.0.0.1"
        if need_external_ip:
            host = get_ip()
        root = self.server_root or \
               os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))),
                            "www")
        rv = FixtureServer(root, host=host)
        rv.start()
        return rv

    def add_test(self, test, expected='pass'):
        filepath = os.path.abspath(test)

        if os.path.isdir(filepath):
            for root, dirs, files in os.walk(filepath):
                for filename in files:
                    if filename.startswith('test_') and (filename.endswith('.py')):
                        filepath = os.path.join(root, filename)
                        self.add_test(filepath)
            return

        testargs = {}
        if self.type is not None:
            testtypes = self.type.replace('+', ' +').replace('-', ' -').split()
            for atype in testtypes:
                if atype.startswith('+'):
                    testargs.update({atype[1:]: 'true'})
                elif atype.startswith('-'):
                    testargs.update({atype[1:]: 'false'})
                else:
                    testargs.update({atype: 'true'})

        file_ext = os.path.splitext(os.path.split(filepath)[-1])[1]

        if file_ext == '.ini':
            manifest = TestManifest()
            manifest.read(filepath)

            filters = []
            if self.test_tags:
                filters.append(tags(self.test_tags))
            manifest_tests = manifest.active_tests(exists=False,
                                                   disabled=True,
                                                   filters=filters,
                                                   device=self.device,
                                                   app=self.appName)
            if len(manifest_tests) == 0:
                self.logger.error("no tests to run using specified "
                                  "combination of filters: {}".format(
                                       manifest.fmt_filters()))

            unfiltered_tests = []
            for test in manifest_tests:
                if test.get('disabled'):
                    self.manifest_skipped_tests.append(test)
                else:
                    unfiltered_tests.append(test)

            target_tests = manifest.get(tests=unfiltered_tests, **testargs)
            for test in unfiltered_tests:
                if test['path'] not in [x['path'] for x in target_tests]:
                    test.setdefault('disabled', 'filtered by type (%s)' % self.type)
                    self.manifest_skipped_tests.append(test)

            for i in target_tests:
                if not os.path.exists(i["path"]):
                    raise IOError("test file: %s does not exist" % i["path"])
                self.add_test(i["path"], i["expected"])
            return

        self.tests.append({'filepath': filepath, 'expected': expected})

    def cleanup(self):
        if self.httpd:
            self.httpd.stop()

        if self.marionette:
            self.marionette.cleanup()

    __del__ = cleanup


def get_ip():
    """Provides an available network interface address, for example
       "192.168.1.3".

       A `NetworkError` exception is raised in case of failure."""

    logger = structuredlog.get_default_logger(component='getIP')

    try:
        hostname = socket.gethostname()
        try:
            logger.debug('Retrieving IP for %s' % hostname)
            ips = socket.gethostbyname_ex(hostname)[2]
        except Exception as e:
            raise e
        if len(ips) == 1:
            ip = ips[0]
        elif len(ips) > 1:
            logger.debug('Multiple addresses found: %s' % ips)
            # no fallback on Windows so take the first address
            ip = ips[0]
        else:
            ip = None
    except socket.gaierror:
        ip = None

    if ip is None:
        raise Exception('Unable to obtain network address')

    return ip
