from __future__ import print_function
import os
import random
import sys
from argparse import ArgumentParser


class GaiaTestArguments(ArgumentParser):
    socket_timeout_default = 360.0

    def __init__(self, **kwargs):
        ArgumentParser.__init__(self, **kwargs)

        def dir_path(path):
            path = os.path.abspath(os.path.expanduser(path))
            if not os.access(path, os.F_OK):
                os.makedirs(path)
            return path

        self.argument_containers = []
        self.add_argument('tests',
                          nargs='*',
                          default=[],
                          help='Tests to run.')
        self.add_argument('--address',
                        help='host:port of running Gecko instance on device to connect to')
        self.add_argument('--device',
                        dest='device_serial',
                        help='serial ID of a device to use for adb / fastboot')
        self.add_argument('--type',
                        help="the type of test to run, can be a combination of values defined in the manifest file; "
                             "individual values are combined with '+' or '-' characters. for example:"
                             " 'smoketest+regression' means the set of tests which are compatible with both smoketest"
                             " and regression")
        self.add_argument('--profile',
                        help='gaia profile to use when launching the gecko process.',
                        type=dir_path)
        self.add_argument('--repeat',
                        type=int,
                        default=0,
                        help='number of times to repeat the test(s)')
        self.add_argument('--testvars',
                        action='append',
                        help='path to a json file with any test data required')
        self.add_argument('--timeout',
                        type=int,
                        help='if a --timeout value is given, it will set the default page load timeout,'
                             'search timeout and script timeout to the given value. If not passed in, '
                             'it will use the default values of 20000ms for page load, 20000ms for search timeout'
                             'and 10000ms for script timeout')
        self.add_argument('--shuffle',
                        action='store_true',
                        default=False,
                        help='run tests in a random order')
        self.add_argument('--shuffle-seed',
                        type=int,
                        default=random.randint(0, sys.maxsize),
                        help='Use given seed to shuffle tests')
        self.add_argument('--server-root',
                        help='url to a webserver or path to a document root from which content '
                        'resources are served (default: {}).'.format(os.path.join(
                            os.path.dirname(os.path.abspath(os.path.dirname(__file__))), 'www')))
        self.add_argument('--logger-name',
                        default='Marionette-based Tests',
                        help='Define the name to associate with the logger used')
        self.add_argument('--socket-timeout',
                        default=self.socket_timeout_default,
                        help='Set the global timeout for marionette socket operations.')
        self.add_argument('--tag',
                        action='append', dest='test_tags',
                        default=None,
                        help="Filter out tests that don't have the given tag. Can be "
                             "used multiple times in which case the test must contain "
                             "at least one of the given tags.")
        self.add_argument('--restart',
                          action='store_true',
                          dest='restart',
                          default=False,
                          help='restart target instance between tests')
        self.add_argument('--filter_type',
                          dest='filter_type',
                          default=None,
                          help="a filter type you can use to determine which type you want to test,"
                               "format is like \"dsds+landscape\"")
        self.add_argument('--tolerance_level',
                          dest='tolerance_level',
                          default=1,
                          help="Define tolerance level."
                               "Level 0: skip some expected results verification to lower down maintenance cost at early phase,"
                               "Level 1: verify all")

    def register_argument_container(self, container):
        group = self.add_argument_group(container.name)

        for cli, kwargs in container.args:
            group.add_argument(*cli, **kwargs)

        self.argument_containers.append(container)

    def parse_args(self, args=None, values=None):
        args = ArgumentParser.parse_args(self, args, values)
        for container in self.argument_containers:
            if hasattr(container, 'parse_args_handler'):
                container.parse_args_handler(args)
        return args

    def verify_usage(self, args):
        if not args.tests:
            print('must specify one or more test files, manifests, or directories')
            sys.exit(1)

        if not args.address and not args.binary:
            print('must specify --binary or --address')
            sys.exit(1)

        for container in self.argument_containers:
            if hasattr(container, 'verify_usage_handler'):
                container.verify_usage_handler(args)

        return args
