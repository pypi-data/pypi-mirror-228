# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import range
from past.builtins import basestring
from builtins import object
import hashlib
import logging
import posixpath
import re
import os
import struct
import io
import tempfile
import time
import zlib

from ..logging.structuredlog import get_default_logger
from ..logging.unstructuredlog import getLogger
from ..mozprocess import ProcessHandler


class DMError(Exception):
    "generic devicemanager exception."

    def __init__(self, msg='', fatal=False):
        self.msg = msg
        self.fatal = fatal

    def __str__(self):
        return self.msg


class KaiOSDeviceManagerADB(object):
    """
    uses the Android "adb" utility to communicate with the device.
    Normally used to communicate with a device that is directly connected with the host machine over a USB port.
    """

    default_timeout = 300
    short_timeout = 30
    _haveRootShell = None
    _haveSu = None
    _suModifier = None
    _lsModifier = None
    _useZip = False
    _logcatNeedsRoot = False
    _pollingInterval = 0.01
    _packageName = None
    _tempDir = None
    _adb_version = None
    _sdk_version = None
    connected = False

    def __init__(self, host=None, port=5555, retryLimit=5, packageName='fennec',
                 adbPath=None, deviceSerial=None, deviceRoot=None,
                 logLevel=logging.ERROR, autoconnect=True, runAdbAsRoot=False,
                 serverHost=None, serverPort=None):
        try:
            self._logger = get_default_logger(component="kaidevice")
            if not self._logger:  # no global structured logger, fall back to reg logging
                self._logger = getLogger("kaidevice")
                if logLevel is not None:
                    self._logger.setLevel(logLevel)
        except AttributeError:
            # Structured logging doesn't work on Python 2.6
            self._logger = None
        self._logLevel = logLevel
        self._remoteIsWin = None
        self._isDeviceRootSetup = False
        self._deviceRoot = deviceRoot

        self.host = host
        self.port = port
        self.retryLimit = retryLimit

        self._serverHost = serverHost
        self._serverPort = serverPort

        # the path to adb, or 'adb' to assume that it's on the PATH
        self._adbPath = adbPath or 'adb'

        # The serial number of the device to use with adb, used in cases
        # where multiple devices are being managed by the same adb instance.
        self._deviceSerial = deviceSerial

        # Some devices do no start adb as root, if allowed you can use
        # this to reboot adbd on the device as root automatically
        self._runAdbAsRoot = runAdbAsRoot

        if packageName:
            self._packageName = packageName

        # verify that we can run the adb command. can't continue otherwise
        self._verifyADB()

        if autoconnect:
            self.connect()

    def _log(self, data):
        """
        This helper function is called by ProcessHandler to log
        the output produced by processes
        """
        self._logger.debug(data)

    @property
    def remoteIsWin(self):
        if self._remoteIsWin is None:
            self._remoteIsWin = self.getInfo("os")["os"][0] == "windows"
        return self._remoteIsWin

    @property
    def logLevel(self):
        return self._logLevel

    @property
    def debug(self):
        self._logger.warning("dm.debug is deprecated. Use logLevel.")
        levels = {logging.DEBUG: 5, logging.INFO: 3, logging.WARNING: 2,
                  logging.ERROR: 1, logging.CRITICAL: 0}
        return levels[self.logLevel]

    @property
    def deviceRoot(self):
        """
        The device root on the device filesystem for putting temporary
        testing files.
        """
        # derive deviceroot value if not set
        if not self._deviceRoot or not self._isDeviceRootSetup:
            self._deviceRoot = self._setupDeviceRoot(self._deviceRoot)
            self._isDeviceRootSetup = True

        return self._deviceRoot

    def connect(self):
        if not self.connected:
            # try to connect to the device over tcp/ip if we have a hostname
            if self.host:
                self._connectRemoteADB()

            # verify that we can connect to the device. can't continue
            self._verifyDevice()

            # Note SDK version
            try:
                proc = self._runCmd(["shell", "getprop", "ro.build.version.sdk"],
                                    timeout=self.short_timeout)
                self._sdk_version = int(proc.output[0])
            except (OSError, ValueError):
                self._sdk_version = 0
            self._logger.info("Detected Android sdk %d" % self._sdk_version)

            # Some commands require root to work properly, even with ADB (e.g.
            # grabbing APKs out of /data). For these cases, we check whether
            # we're running as root. If that isn't true, check for the
            # existence of an su binary
            self._checkForRoot()

    def __del__(self):
        if self.host:
            self._disconnectRemoteADB()

    def shell(self, cmd, outputfile, env=None, cwd=None, timeout=None, root=False):
        # FIXME: this function buffers all output of the command into memory,
        # always. :(

        # If requested to run as root, check that we can actually do that
        if root:
            if self._haveRootShell is None and self._haveSu is None:
                self._checkForRoot()
            if not self._haveRootShell and not self._haveSu:
                raise DMError(
                    "Shell command '%s' requested to run as root but root "
                    "is not available on this device. Root your device or "
                    "refactor the test/harness to not require root." %
                    self._escapedCommandLine(cmd))

        # Getting the return code is more complex than you'd think because adb
        # doesn't actually return the return code from a process, so we have to
        # capture the output to get it
        if root and self._haveSu:
            print("root access")
            cmdline = "su %s \"%s\"" % (self._suModifier,
                                        self._escapedCommandLine(cmd))
        else:
            print("without root access")
            cmdline = self._escapedCommandLine(cmd)
        cmdline += "; echo $?"

        # prepend cwd and env to command if necessary
        if cwd:
            print("IN CWD")
            cmdline = "cd %s; %s" % (cwd, cmdline)
        if env:
            print("IN ENV")
            envstr = '; '.join(['export %s=%s' % (x[0], x[1]) for x in iter(env.items())])
            cmdline = envstr + "; " + cmdline

        # all output should be in stdout
        args = [self._adbPath]
        if self._serverHost is not None:
            args.extend(['-H', self._serverHost])
        if self._serverPort is not None:
            args.extend(['-P', str(self._serverPort)])
        if self._deviceSerial:
            args.extend(['-s', self._deviceSerial])
        args.extend(["shell", cmdline])

        def _timeout():
            self._logger.error("Timeout exceeded for shell call '%s'" % ' '.join(args))

        self._logger.debug("shell - command: %s" % ' '.join(args))
        proc = ProcessHandler(args, processOutputLine=self._log, onTimeout=_timeout)

        if not timeout:
            # We are asserting that all commands will complete in this time unless
            # otherwise specified
            timeout = self.default_timeout

        timeout = int(timeout)
        proc.run(timeout)
        proc.wait()
        output = proc.output
        print("output", output[:30])

        if output:
            lastline = output[-1]
            print('lastline', lastline)
            if lastline:
                m = re.search(b'([0-9]+)', lastline)
                if m:
                    print("inside if")
                    return_code = m.group(1)
                    print("return code", return_code)
                    
                    for line in output:
                        outputfile.write(line)
                    print("final", outputfile.getvalue()[:30])
                    print(type(outputfile))
                    outputfile.seek(-1, 1)
                    outputfile.truncate()  # truncate off the return code
                    print("final2", outputfile.getvalue()[:30])
                    return int(return_code)

        return None

    def shellCheckOutput(self, cmd, env=None, cwd=None, timeout=None, root=False):
        """
        Executes shell command on device and returns output as a string. Raises if
        the return code is non-zero.

        :param cmd: Commandline list to execute
        :param env: Environment to pass to exec command
        :param cwd: Directory to execute command from
        :param timeout: specified in seconds, defaults to 'default_timeout'
        :param root: Specifies whether command requires root privileges
        :raises: DMError
        """
        print("now here in sell")
        buf = io.BytesIO()
        retval = self.shell(cmd, buf, env=env, cwd=cwd, timeout=timeout, root=root)
        print("retval", retval)
        output = buf.getvalue().decode('utf-8').rstrip('\n')
        print(type(output))
        print("real output", output[:30])
        buf.close()
        if retval != 0:
            raise DMError(
                "Non-zero return code for command: %s "
                "(output: '%s', retval: '%s')" % (cmd, output, retval))
        return output

    def forward(self, local, remote):
        """
        Forward socket connections.

        Forward specs are one of:
          tcp:<port>
          localabstract:<unix domain socket name>
          localreserved:<unix domain socket name>
          localfilesystem:<unix domain socket name>
          dev:<character device name>
          jdwp:<process pid> (remote only)
        """
        if not self._checkCmd(['forward', local, remote], timeout=self.short_timeout) == 0:
            raise DMError("Failed to forward socket connection.")

    def remove_forward(self, local=None):
        """
        Turn off forwarding of socket connection.
        """
        cmd = ['forward']
        if local is None:
            cmd.extend(['--remove-all'])
        else:
            cmd.extend(['--remove', local])
        if not self._checkCmd(cmd, timeout=self.short_timeout) == 0:
            raise DMError("Failed to remove connection forwarding.")

    def remount(self):
        "Remounts the /system partition on the device read-write."
        return self._checkCmd(['remount'], timeout=self.short_timeout)

    def devices(self):
        "Return a list of connected devices as (serial, status) tuples."
        proc = self._runCmd(['devices'])
        proc.output.pop(0)  # ignore first line of output
        devices = []
        for line in proc.output:
            result = re.match('(.*?)\t(.*)', line)
            if result:
                devices.append((result.group(1), result.group(2)))
        return devices

    def _connectRemoteADB(self):
        self._checkCmd(["connect", self.host + ":" + str(self.port)])

    def _disconnectRemoteADB(self):
        self._checkCmd(["disconnect", self.host + ":" + str(self.port)])

    def pushFile(self, localname, destname, retryLimit=None, createDir=True):
        # you might expect us to put the file *in* the directory in this case,
        # but that would be inconsistent with historical behavior.
        retryLimit = retryLimit or self.retryLimit
        if self.dirExists(destname):
            raise DMError("Attempted to push a file (%s) to a directory (%s)!" %
                          (localname, destname))
        if not os.access(localname, os.F_OK):
            raise DMError("File not found: %s" % localname)

        proc = self._runCmd(["push", os.path.realpath(localname), destname],
                            retryLimit=retryLimit)
        if proc.returncode != 0:
            raise DMError("Error pushing file %s -> %s; output: %s" %
                          (localname, destname, proc.output))

    def mkDir(self, name):
        result = self._runCmd(["shell", "mkdir", name], timeout=self.short_timeout).output
        if len(result) and 'read-only file system' in result[0].lower():
            raise DMError("Error creating directory: read only file system")

    def mkDirs(self, filename):
        """
        Make directory structure on the device.

        WARNING: does not create last part of the path. For example, if asked to
        create `/mnt/sdcard/foo/bar/baz`, it will only create `/mnt/sdcard/foo/bar`
        """
        filename = posixpath.normpath(filename)
        containing = posixpath.dirname(filename)
        if not self.dirExists(containing):
            parts = filename.split('/')
            name = "/" if not self.remoteIsWin else parts.pop(0)
            for part in parts[:-1]:
                if part != "":
                    name = posixpath.join(name, part)
                    self.mkDir(name)  # mkDir will check previous existence

    def dirExists(self, remotePath):
        self._detectLsModifier()
        data = self._runCmd(["shell", "ls", self._lsModifier, remotePath + '/'],
                            timeout=self.short_timeout).output

        if len(data) == 1:
            res = data[0]
            if "Not a directory" in res or "No such file or directory" in res:
                return False
        return True

    def fileExists(self, filepath):
        self._detectLsModifier()
        data = self._runCmd(["shell", "ls", self._lsModifier, filepath],
                            timeout=self.short_timeout).output
        if len(data) == 1:
            foundpath = data[0].decode('utf-8').rstrip()
            if foundpath == filepath:
                return True
        return False

    def removeFile(self, filename):
        if self.fileExists(filename):
            self._checkCmd(["shell", "rm", filename], timeout=self.short_timeout)

    def removeDir(self, remoteDir):
        if self.dirExists(remoteDir):
            self._checkCmd(["shell", "rm", "-r", remoteDir], timeout=self.short_timeout)
        else:
            self.removeFile(remoteDir.strip())

    def moveTree(self, source, destination):
        self._checkCmd(["shell", "mv", source, destination], timeout=self.short_timeout)

    def copyTree(self, source, destination):
        self._checkCmd(["shell", "dd", "if=%s" % source, "of=%s" % destination])

    def listFiles(self, rootdir):
        self._detectLsModifier()
        data = self._runCmd(["shell", "ls", self._lsModifier, rootdir],
                            timeout=self.short_timeout).output
        data[:] = [item.rstrip('\r\n') for item in data]
        if (len(data) == 1):
            if (data[0] == rootdir):
                return []
            if (data[0].find("No such file or directory") != -1):
                return []
            if (data[0].find("Not a directory") != -1):
                return []
            if (data[0].find("Permission denied") != -1):
                return []
            if (data[0].find("opendir failed") != -1):
                return []
            if (data[0].find("Device or resource busy") != -1):
                return []
        return data

    def getProcessList(self):
        ret = []
        p = self._runCmd(["shell", "ps"], timeout=self.short_timeout)
        if not p or not p.output or len(p.output) < 1:
            return ret
        # first line is the headers
        p.output.pop(0)
        for proc in p.output:
            els = proc.split()
            # We need to figure out if this is "user pid name" or
            # "pid user vsz stat command"
            if els[1].isdigit():
                ret.append(list([int(els[1]), els[len(els) - 1], els[0]]))
            else:
                ret.append(list([int(els[0]), els[len(els) - 1], els[1]]))
        return ret

    def processInfo(self, processName):
        """
        Returns information on the process with processName.
        Information on process is in tuple format: (pid, process path, user)
        If a process with the specified name does not exist this function will return None.
        """
        if not isinstance(processName, basestring):
            raise TypeError("Process name %s is not a string" % processName)

        processInfo = None

        # filter out extra spaces
        parts = [x for x in processName.split(' ') if x != '']
        processName = ' '.join(parts)

        # filter out the quoted env string if it exists
        # ex: '"name=value;name2=value2;etc=..." process args' -> 'process args'
        parts = processName.split('"')
        if (len(parts) > 2):
            processName = ' '.join(parts[2:]).strip()

        pieces = processName.split(' ')
        parts = pieces[0].split('/')
        app = parts[-1]

        procList = self.getProcessList()
        if (procList == []):
            return None

        for proc in procList:
            procName = proc[1].split('/')[-1]
            if (procName == app):
                processInfo = proc
                break
        return processInfo

    def processExist(self, processName):
        """
        Returns True if process with name processName is running on device.
        """
        processInfo = self.processInfo(processName)
        if processInfo:
            return processInfo[0]

    def fireProcess(self, appname, failIfRunning=False):
        """
        Starts a process

        returns: pid

        DEPRECATED: Use shell() or launchApplication() for new code
        """
        # strip out env vars
        parts = appname.split('"')
        if (len(parts) > 2):
            parts = parts[2:]
        return self.launchProcess(parts, failIfRunning)

    def launchProcess(self, cmd, outputFile="process.txt", cwd='', env='', failIfRunning=False):
        """
        Launches a process, redirecting output to standard out

        WARNING: Does not work how you expect on Android! The application's
        own output will be flushed elsewhere.

        DEPRECATED: Use shell() or launchApplication() for new code
        """
        if cmd[0] == "am":
            self._checkCmd(["shell"] + cmd)
            return outputFile

        acmd = ["-W"]
        cmd = ' '.join(cmd).strip()
        i = cmd.find(" ")
        re_url = re.compile('^[http|file|chrome|about].*')
        last = cmd.rfind(" ")
        uri = ""
        args = ""
        if re_url.match(cmd[last:].strip()):
            args = cmd[i:last].strip()
            uri = cmd[last:].strip()
        else:
            args = cmd[i:].strip()
        acmd.append("-n")
        acmd.append(cmd[0:i] + "/org.mozilla.gecko.BrowserApp")
        if args != "":
            acmd.append("--es")
            acmd.append("args")
            acmd.append(args)
        if env != '' and env is not None:
            envCnt = 0
            # env is expected to be a dict of environment variables
            for envkey, envval in env.items():
                acmd.append("--es")
                acmd.append("env" + str(envCnt))
                acmd.append(envkey + "=" + envval)
                envCnt += 1
        if uri != "":
            acmd.append("-d")
            acmd.append(uri)

        acmd = ["shell", ' '.join(['"' + x + '"' for x in ["am", "start"] + acmd])]
        self._logger.info(acmd)
        self._checkCmd(acmd)
        return outputFile

    def _runPull(self, remoteFile, localFile):
        """
        Pulls remoteFile from device to host
        """
        try:
            self._runCmd(["pull",  remoteFile, localFile])
        except (OSError, ValueError):
            raise DMError("Error pulling remote file '%s' to '%s'" % (remoteFile, localFile))

    def pullFile(self, remoteFile, offset=None, length=None):
        # might not support Windows
        with tempfile.NamedTemporaryFile() as tf:
            self._runPull(remoteFile, tf.name)
            # we need to reopen the file to get the written contents
            with open(tf.name) as tf2:
                # ADB pull does not support offset and length, but we can
                # instead read only the requested portion of the local file
                if offset is not None and length is not None:
                    tf2.seek(offset)
                    return tf2.read(length)
                elif offset is not None:
                    tf2.seek(offset)
                    return tf2.read()
                else:
                    return tf2.read()

    def getFile(self, remoteFile, localFile):
        self._runPull(remoteFile, localFile)

    def validateFile(self, remoteFile, localFile):
        md5Remote = self._getRemoteHash(remoteFile)
        md5Local = self._getLocalHash(localFile)
        if md5Remote is None or md5Local is None:
            return None
        return md5Remote == md5Local

    def validateDir(self, localDirname, remoteDirname):
        """
        Returns True if remoteDirname on device is same as localDirname on host.
        """

        self._logger.info("validating directory: %s to %s" % (localDirname, remoteDirname))
        for root, dirs, files in os.walk(localDirname):
            parts = root.split(localDirname)
            for f in files:
                remoteRoot = remoteDirname + '/' + parts[1]
                remoteRoot = remoteRoot.replace('/', '/')
                if (parts[1] == ""):
                    remoteRoot = remoteDirname
                remoteName = remoteRoot + '/' + f
                if (self.validateFile(remoteName, os.path.join(root, f)) is not True):
                    return False
        return True

    def _getRemoteHash(self, remoteFile):
        """
        Return the md5 sum of a file on the device
        """
        with tempfile.NamedTemporaryFile() as f:
            self._runPull(remoteFile, f.name)

            return self._getLocalHash(f.name)

    @staticmethod
    def _getLocalHash(filename):
        """
        Return the MD5 sum of a file on the host.
        """
        f = open(filename, 'rb')
        if f is None:
            return None

        try:
            mdsum = hashlib.md5()
        except:
            return None

        while 1:
            data = f.read(1024)
            if not data:
                break
            mdsum.update(data)

        f.close()
        hexval = mdsum.hexdigest()
        return hexval

    @staticmethod
    def _escapedCommandLine(cmd):
        """
        Utility function to return escaped and quoted version of command line.
        """
        quotedCmd = []

        for arg in cmd:
            arg.replace('&', '\&')

            needsQuoting = False
            for char in [' ', '(', ')', '"', '&']:
                if arg.find(char) >= 0:
                    needsQuoting = True
                    break
            if needsQuoting:
                arg = '\'%s\'' % arg

            quotedCmd.append(arg)
            print("cmd data", quotedCmd)

        return " ".join(quotedCmd)

    def _setupDeviceRoot(self, deviceRoot):
        # user-specified device root, create it and return it
        if deviceRoot:
            self.mkDir(deviceRoot)
            return deviceRoot

        # we must determine the device root ourselves
        paths = [('/storage/sdcard0', 'tests'),
                 ('/storage/sdcard1', 'tests'),
                 ('/storage/sdcard', 'tests'),
                 ('/mnt/sdcard', 'tests'),
                 ('/sdcard', 'tests'),
                 ('/data/local', 'tests')]
        for (basePath, subPath) in paths:
            if self.dirExists(basePath):
                root = os.path.join(basePath, subPath)
                try:
                    self.mkDir(root)
                    return root
                except:
                    pass

        raise DMError("Unable to set up device root using paths: [%s]"
                      % ", ".join(["'%s'" % os.path.join(b, s) for b, s in paths]))

    def reboot(self, wait=False, **kwargs):
        self._checkCmd(["reboot"])
        if wait:
            self._checkCmd(["wait-for-device"])
            if self._runAdbAsRoot:
                self._adb_root()
            self._checkCmd(["shell", "ls", "/sbin"], timeout=self.short_timeout)

    def updateApp(self, appBundlePath, **kwargs):
        return self._runCmd(["install", "-r", appBundlePath]).output

    def getCurrentTime(self):
        timestr = str(self._runCmd(["shell", "date", "+%s"], timeout=self.short_timeout).output[0])
        if (not timestr or not timestr.isdigit()):
            raise DMError("Unable to get current time using date (got: '%s')" % timestr)
        return int(timestr) * 1000

    def getInfo(self, directive=None):
        directive = directive or "all"
        ret = {}
        if directive == "id" or directive == "all":
            ret["id"] = self._runCmd(["get-serialno"], timeout=self.short_timeout).output[0].decode("utf-8")
            print("1", dict(list(ret.items())[0:2]))
        if directive == "os" or directive == "all":
            ret["os"] = self.shellCheckOutput(
                ["getprop", "ro.build.display.id"], timeout=self.short_timeout)
            print("2", dict(list(ret.items())[0:2]))
            if not ret["os"]:
                raise DMError('error getting os info (getprop ro.build.display.id)')
        if directive == "uptime" or directive == "all":
            uptime = self.shellCheckOutput(["uptime"], timeout=self.short_timeout)
            print("3", dict(list(ret.items())[0:2]))
            if not uptime:
                raise DMError("error getting uptime")
            m = re.match("up time: ((\d+) days, )*(\d{2}):(\d{2}):(\d{2})", uptime)
            if m:
                uptime = "%d days %d hours %d minutes %d seconds" % tuple(
                    [int(g or 0) for g in m.groups()[1:]])
            ret["uptime"] = uptime
            print("4", dict(list(ret.items())[0:2]))
        if directive == "process" or directive == "all":
            data = self.shellCheckOutput(["ps"], timeout=self.short_timeout)
            ret["process"] = data.split('\n')
            print("5", dict(list(ret.items())[0:2]))
        if directive == "systime" or directive == "all":
            ret["systime"] = self.shellCheckOutput(["date"], timeout=self.short_timeout)
            print("6", dict(list(ret.items())[0:2]))
        if directive == "memtotal" or directive == "all":
            meminfo = {}
            for line in self.pullFile("/proc/meminfo").splitlines():
                key, value = line.split(":")
                meminfo[key] = value.strip()
            ret["memtotal"] = meminfo["MemTotal"]
            print("7", dict(list(ret.items())[0:2]))
        if directive == "disk" or directive == "all":
            data = self.shellCheckOutput(
                ["df", "/data", "/system"], timeout=self.short_timeout)
            ret["disk"] = data.split('\n')
            print("8", dict(list(ret.items())[0:2]))
        self._logger.debug("getInfo: %s" % ret)
        return ret

    def uninstallApp(self, appName, installPath=None):
        status = self._runCmd(["uninstall", appName]).output[0].strip()
        if status != 'Success':
            raise DMError("uninstall failed for %s. Got: %s" % (appName, status))

    def uninstallAppAndReboot(self, appName, installPath=None):
        self.uninstallApp(appName)
        self.reboot()

    def _runCmd(self, args, timeout=None, retryLimit=None):
        """
        Runs a command using adb
        If timeout is specified, the process is killed after <timeout> seconds.

        returns: instance of ProcessHandler
        """
        retryLimit = retryLimit or self.retryLimit
        finalArgs = [self._adbPath]
        if self._serverHost is not None:
            finalArgs.extend(['-H', self._serverHost])
        if self._serverPort is not None:
            finalArgs.extend(['-P', str(self._serverPort)])
        if self._deviceSerial:
            finalArgs.extend(['-s', self._deviceSerial])
        finalArgs.extend(args)
        self._logger.debug("_runCmd - command: %s" % ' '.join(finalArgs).encode('utf-8'))
        if not timeout:
            timeout = self.default_timeout

        def _timeout():
            self._logger.error("Timeout exceeded for _runCmd call '%s'" % ' '.join(finalArgs))

        retries = 0
        while retries < retryLimit:
            proc = ProcessHandler(finalArgs, storeOutput=True,
                                  processOutputLine=self._log, onTimeout=_timeout)
            proc.run(timeout=timeout)
            proc.returncode = proc.wait()
            if proc.returncode is None:
                proc.kill()
                retries += 1
            else:
                return proc

    # timeout is specified in seconds, and if no timeout is given,
    # we will run until we hit the default_timeout specified in the __init__
    def _checkCmd(self, args, timeout=None, retryLimit=None):
        """
        Runs a command using adb and waits for the command to finish.
        If timeout is specified, the process is killed after <timeout> seconds.

        returns: returncode from process
        """
        retryLimit = retryLimit or self.retryLimit
        finalArgs = [self._adbPath]
        if self._serverHost is not None:
            finalArgs.extend(['-H', self._serverHost])
        if self._serverPort is not None:
            finalArgs.extend(['-P', str(self._serverPort)])
        if self._deviceSerial:
            finalArgs.extend(['-s', self._deviceSerial])
        finalArgs.extend(args)
        self._logger.debug("_checkCmd - command: %s" % ' '.join(finalArgs))
        if not timeout:
            # We are asserting that all commands will complete in this
            # time unless otherwise specified
            timeout = self.default_timeout

        def _timeout():
            self._logger.error("Timeout exceeded for _checkCmd call '%s'" % ' '.join(finalArgs))

        timeout = int(timeout)
        retries = 0
        while retries < retryLimit:
            proc = ProcessHandler(finalArgs, processOutputLine=self._log, onTimeout=_timeout)
            proc.run(timeout=timeout)
            ret_code = proc.wait()
            if ret_code is None:
                proc.kill()
                retries += 1
            else:
                return ret_code

        raise DMError("Timeout exceeded for _checkCmd call after %d retries." % retries)

    def chmodDir(self, remoteDir, mask="777"):
        if (self.dirExists(remoteDir)):
            if '/sdcard' in remoteDir:
                self._logger.debug("chmod %s -- skipped (/sdcard)" % remoteDir)
            else:
                files = self.listFiles(remoteDir.strip())
                for f in files:
                    remoteEntry = remoteDir.strip() + "/" + f.strip()
                    if (self.dirExists(remoteEntry)):
                        self.chmodDir(remoteEntry)
                    else:
                        self._checkCmd(["shell", "chmod", mask, remoteEntry],
                                       timeout=self.short_timeout)
                        self._logger.info("chmod %s" % remoteEntry)
                self._checkCmd(["shell", "chmod", mask, remoteDir], timeout=self.short_timeout)
                self._logger.debug("chmod %s" % remoteDir)
        else:
            self._checkCmd(["shell", "chmod", mask, remoteDir.strip()], timeout=self.short_timeout)
            self._logger.debug("chmod %s" % remoteDir.strip())

    def _verifyADB(self):
        """
        Check to see if adb itself can be executed.
        # """
        if self._adbPath != 'adb':
            if not os.access(self._adbPath, os.X_OK):
                raise DMError("invalid adb path, or adb not executable: %s" % self._adbPath)

        try:
            re_version = re.compile(r'Android Debug Bridge version (.*)')
            proc = self._runCmd(["version"], timeout=self.short_timeout)
            self._adb_version = re_version.match(proc.output[0].decode("utf-8")).group(1)
            self._logger.info("Detected adb %s" % self._adb_version)
        except os.error as err:
            raise DMError(
                "unable to execute ADB (%s): ensure Android SDK is installed "
                "and adb is in your $PATH" % err)

    def _verifyDevice(self):
        # If there is a device serial number, see if adb is connected to it
        if self._deviceSerial:
            deviceStatus = None
            devices = self._runCmd(["devices"])
            for line in self._runCmd(["devices"]).output:
                m = re.match('(.+)?\s+(.+)$', line.decode("utf-8"))
                if m:
                    print(m.group(1))
                    if self._deviceSerial == m.group(1):
                        deviceStatus = m.group(2)
            if deviceStatus is None:
                raise DMError("device not found: %s" % self._deviceSerial)
            elif deviceStatus != "device":
                raise DMError("bad status for device %s: %s" % (self._deviceSerial, deviceStatus))

        # Check to see if we can connect to device and run a simple command
        if not self._checkCmd(["shell", "echo"], timeout=self.short_timeout) == 0:
            raise DMError("unable to connect to device")

    def _checkForRoot(self):
        self._haveRootShell = False
        self._haveSu = False
        # If requested to attempt to run adbd as root, do so before
        # checking whether adbs is running as root.
        if self._runAdbAsRoot:
            self._adb_root()

        # Check whether we _are_ root by default (some development boards work
        # this way, this is also the result of some relatively rare rooting
        # techniques)
        proc = self._runCmd(["shell", "id"], timeout=self.short_timeout)
        if proc.output and b'uid=0(root)' in proc.output[0]:
            self._haveRootShell = True
            # if this returns true, we don't care about su
            return

        # if root shell is not available, check if 'su' can be used to gain
        # root
        def su_id(su_modifier, timeout):
            proc = self._runCmd(["shell", "su", su_modifier, "id"],
                                timeout=timeout)

            # wait for response for maximum of 15 seconds, in case su
            # prompts for a password or triggers the Android SuperUser
            # prompt
            start_time = time.time()
            retcode = None
            while (time.time() - start_time) <= 15 and retcode is None:
                retcode = proc.poll()
            if retcode is None:  # still not terminated, kill
                proc.kill()

            if proc.output and 'uid=0(root)' in proc.output[0]:
                return True
            return False

        if su_id('0', self.short_timeout):
            self._haveSu = True
            self._suModifier = '0'
        elif su_id('-c', self.short_timeout):
            self._haveSu = True
            self._suModifier = '-c'

    def _adb_root(self):
        """ Some devices require us to reboot adbd as root.
            This function takes care of it.
        """
        if self.processInfo("adbd")[2] != "root":
            self._checkCmd(["root"])
            self._checkCmd(["wait-for-device"])
            if self.processInfo("adbd")[2] != "root":
                raise DMError("We tried rebooting adbd as root, however, it failed.")

    def _detectLsModifier(self):
        if self._lsModifier is None:
            # Check if busybox -1A is required in order to get one
            # file per line.
            output = self._runCmd(["shell", "ls", "-1A", "/"],
                                  timeout=self.short_timeout).output
            output = b' '.join(output)
            if b'error: device not found' in output:
                raise DMError(output)
            if b"Unknown option '-1'. Aborting." in output:
                self._lsModifier = "-a"
            elif b"No such file or directory" in output:
                self._lsModifier = "-a"
            else:
                self._lsModifier = "-1A"

    def getIP(self, interfaces=['eth0', 'wlan0']):
        """
        Returns the IP of the device, or None if no connection exists.
        """
        for interface in interfaces:
            match = re.match(r"%s: ip (\S+)" % interface,
                             self.shellCheckOutput(['ifconfig', interface],
                                                   timeout=self.short_timeout))
            if match:
                return match.group(1)

    def recordLogcat(self):
        """
        Clears the logcat file making it easier to view specific events.
        """
        # TODO: spawn this off in a separate thread/process so we can collect all
        # the logcat information

        # Right now this is just clearing the logcat so we can only see what
        # happens after this call.
        self.shellCheckOutput(['/system/bin/logcat', '-c'], root=self._logcatNeedsRoot,
                              timeout=self.short_timeout)

    def getLogcat(self, filterSpecs=["dalvikvm:I", "ConnectivityService:S",
                                     "WifiMonitor:S", "WifiStateTracker:S",
                                     "wpa_supplicant:S", "NetworkStateTracker:S"],
                  format="time",
                  filterOutRegexps=[]):
        """
        Returns the contents of the logcat file as a list of
        '\n' terminated strings
        """
        cmdline = ["/system/bin/logcat", "-v", format, "-d"] + filterSpecs
        output = self.shellCheckOutput(cmdline,
                                       root=self._logcatNeedsRoot,
                                       timeout=self.short_timeout)
        lines = output.replace('\r\n', '\n').splitlines(True)

        for regex in filterOutRegexps:
            lines = [line for line in lines if not re.search(regex, line)]

        return lines

    def saveScreenshot(self, filename):
        """
        Takes a screenshot of what's being display on the device. Uses
        "screencap" on newer (Android 3.0+) devices (and some older ones with
        the functionality backported). This function also works on B2G.

        Throws an exception on failure. This will always fail on devices
        without the screencap utility.
        """
        screencap = '/system/bin/screencap'
        if not self.fileExists(screencap):
            raise DMError("Unable to capture screenshot on device: no screencap utility")

        with open(filename, 'w') as pngfile:
            # newer versions of screencap can write directly to a png, but some
            # older versions can't
            tempScreenshotFile = self.deviceRoot + "/ss-dm.tmp"
            self.shellCheckOutput(["sh", "-c", "%s > %s" %
                                   (screencap, tempScreenshotFile)],
                                  root=True)
            buf = self.pullFile(tempScreenshotFile)
            width = int(struct.unpack("I", buf[0:4])[0])
            height = int(struct.unpack("I", buf[4:8])[0])
            with open(filename, 'w') as pngfile:
                pngfile.write(self._writePNG(buf[12:], width, height))
            self.removeFile(tempScreenshotFile)

    @staticmethod
    def _writePNG(buf, width, height):
        """
        Method for writing a PNG from a buffer, used by getScreenshot on older devices,
        """
        # Based on: http://code.activestate.com/recipes/577443-write-a-png-image-in-native-python/
        width_byte_4 = width * 4
        raw_data = b"".join(b'\x00' + buf[span:span + width_byte_4]
                            for span in range(0, (height - 1) * width * 4, width_byte_4))

        def png_pack(png_tag, data):
            chunk_head = png_tag + data
            return struct.pack("!I", len(data)) \
                + chunk_head \
                + struct.pack("!I", 0xFFFFFFFF & zlib.crc32(chunk_head))
        return b"".join([
            b'\x89PNG\r\n\x1a\n',
            png_pack(b'IHDR', struct.pack("!2I5B", width, height, 8, 6, 0, 0, 0)),
            png_pack(b'IDAT', zlib.compress(raw_data, 9)),
            png_pack(b'IEND', b'')])
