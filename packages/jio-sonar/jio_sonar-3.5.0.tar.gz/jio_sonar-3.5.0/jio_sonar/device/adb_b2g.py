# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import traceback
import os
from adb import ADBDevice, ADBError


class ADBB2G(ADBDevice):
    """ADBB2G implements :class:`ADBDevice` providing B2G-specific
    functionality.

    ::

       from mozdevice import ADBB2G

       adbdevice = ADBB2G()
       print adbdevice.list_files("/mnt/sdcard")
       if adbdevice.process_exist("b2g"):
           print "B2G is running"
    """

    def get_battery_percentage(self, timeout=None):
        """Returns the battery charge as a percentage.

        :param timeout: optional integer specifying the maximum time in
            seconds for any spawned adb process to complete before
            throwing an ADBTimeoutError.
            This timeout is per adb call. The total time spent
            may exceed this value. If it is not specified, the value
            set in the ADBDevice constructor is used.
        :returns: battery charge as a percentage.
        :raises: * ADBTimeoutError
                 * ADBError
        """
        with NamedTemporaryFile() as tf:
            self.pull('/sys/class/power_supply/battery/capacity', tf.name,
                      timeout=timeout)
            try:
                with open(tf.name) as tf2:
                    return tf2.read().splitlines()[0]
            except Exception as e:
                raise ADBError(traceback.format_exception_only(
                    type(e), e)[0].strip())

    def get_memory_total(self, timeout=None):
        """Returns the total memory available with units.

        :param timeout: optional integer specifying the maximum time in
            seconds for any spawned adb process to complete before
            throwing an ADBTimeoutError.
            This timeout is per adb call. The total time spent
            may exceed this value. If it is not specified, the value
            set in the ADBDevice constructor is used.
        :returns: memory total with units.
        :raises: * ADBTimeoutError
                 * ADBError
        """
        meminfo = {}
        with NamedTemporaryFile() as tf:
            self.pull('/proc/meminfo', tf.name, timeout=timeout)
            try:
                with open(tf.name) as tf2:
                    for line in tf2.read().splitlines():
                        key, value = line.split(':')
                        meminfo[key] = value.strip()
            except Exception as e:
                raise ADBError(traceback.format_exception_only(
                    type(e), e)[0].strip())
        return meminfo['MemTotal']

    def get_info(self, directive=None, timeout=None):
        """
        Returns a dictionary of information strings about the device.

        :param directive: information you want to get. Options are:
             - `battery` - battery charge as a percentage
             - `disk` - total, free, available bytes on disk
             - `id` - unique id of the device
             - `memtotal` - total memory available on the device
             - `os` - name of the os
             - `process` - list of running processes (same as ps)
             - `systime` - system time of the device
             - `uptime` - uptime of the device

            If `directive` is `None`, will return all available information
        :param timeout: optional integer specifying the maximum time in
            seconds for any spawned adb process to complete before
            throwing an ADBTimeoutError.
            This timeout is per adb call. The total time spent
            may exceed this value. If it is not specified, the value
            set in the ADB constructor is used.
        :raises: * ADBTimeoutError
                 * ADBError
        """
        info = super(ADBB2G, self).get_info(directive=directive,
                                            timeout=timeout)

        directives = ['memtotal']
        if directive in directives:
            directives = [directive]

        if 'memtotal' in directives:
            info['memtotal'] = self.get_memory_total(timeout=timeout)
        return info

    def is_device_ready(self, timeout=None):
        """Returns True if the device is ready.

        :param timeout: optional integer specifying the maximum time in
            seconds for any spawned adb process to complete before
            throwing an ADBTimeoutError.
            This timeout is per adb call. The total time spent
            may exceed this value. If it is not specified, the value
            set in the ADB constructor is used.
        :raises: * ADBTimeoutError
                 * ADBError
        """
        return self.shell_bool('ls /sbin', timeout=timeout)


class NamedTemporaryFile(object):
    """
    Like tempfile.NamedTemporaryFile except it works on Windows
    in the case where you open the created file a second time.

    This behaves very similarly to tempfile.NamedTemporaryFile but may
    not behave exactly the same. For example, this function does not
    prevent fd inheritance by children.

    Example usage:

    with NamedTemporaryFile() as fh:
        fh.write(b'foobar')

        print('Filename: %s' % fh.name)

    see https://bugzilla.mozilla.org/show_bug.cgi?id=821362
    """
    def __init__(self, mode='w+b', bufsize=-1, suffix='', prefix='tmp',
                 dir=None, delete=True):

        import tempfile
        fd, path = tempfile.mkstemp(suffix, prefix, dir, 't' in mode)
        os.close(fd)

        self.file = open(path, mode)
        self._path = path
        self._delete = delete
        self._unlinked = False

    def __getattr__(self, k):
        return getattr(self.__dict__['file'], k)

    def __iter__(self):
        return self.__dict__['file']

    def __enter__(self):
        self.file.__enter__()
        return self

    def __exit__(self, exc, value, tb):
        self.file.__exit__(exc, value, tb)
        if self.__dict__['_delete']:
            os.unlink(self.__dict__['_path'])
            self._unlinked = True

    def __del__(self):
        if self.__dict__['_unlinked']:
            return
        self.file.__exit__(None, None, None)
        if self.__dict__['_delete']:
            os.unlink(self.__dict__['_path'])
