from future import standard_library
standard_library.install_aliases()
from builtins import object
import configparser
import os
import re
import tempfile
import xml.dom.minidom
import zipfile
from ..logging.structuredlog import get_default_logger
from ..logging.unstructuredlog import getLogger

from .adbmanager import KaiOSDeviceManagerADB

INI_DATA_MAPPING = (('application', 'App'), ('platform', 'Build'))


def get_version(sources=None, dm=None, device_serial=None, adb_host=None, adb_port=None):
    version = KaiOSVersion(sources=sources, dm=dm,
                           device_serial=device_serial, adb_host=adb_host, adb_port=adb_port)

    for (key, value) in sorted(version._info.items()):
        if value:
            version._logger.info('%s: %s' % (key, value))

    return version._info


class KaiOSVersion(object):

    def __init__(self, sources=None, dm=None, device_serial=None, adb_host=None, adb_port=None):
        self._info = {}
        self._logger = get_default_logger(component='kaiversion')
        if not self._logger:
            self._logger = getLogger('kaiversion')

        sources = sources or \
            os.path.exists(os.path.join(os.getcwd(), 'sources.xml')) and \
            os.path.join(os.getcwd(), 'sources.xml')

        if sources and os.path.exists(sources):
            sources_xml = xml.dom.minidom.parse(sources)
            for element in sources_xml.getElementsByTagName('project'):
                path = element.getAttribute('path')
                changeset = element.getAttribute('revision')
                if path in ['gaia', 'gecko', 'build']:
                    if path == 'gaia' and self._info.get('gaia_changeset'):
                        break
                    self._info['_'.join([path, 'changeset'])] = changeset

        if not dm:
            dm = KaiOSDeviceManagerADB(deviceSerial=device_serial,
                                            serverHost=adb_host,
                                            serverPort=adb_port)

        tempdir = tempfile.mkdtemp()
        for ini in ('application', 'platform'):
            with open(os.path.join(tempdir, '%s.ini' % ini), 'w') as f:
                f.write(dm.pullFile('/system/b2g/%s.ini' % ini))
                f.flush()
        self.get_gecko_info(tempdir)

        for path in ['/system/b2g', '/data/local']:
            path += '/webapps/settings.gaiamobile.org/application.zip'
            if dm.fileExists(path):
                with tempfile.NamedTemporaryFile() as f:
                    dm.getFile(path, f.name)
                    self.get_gaia_info(f)
                break
        else:
            self._logger.warning('Error pulling gaia file')

        build_props = dm.pullFile('/system/build.prop')
        desired_props = {
            'ro.build.version.incremental': 'device_firmware_version_incremental',
            'ro.build.version.release': 'device_firmware_version_release',
            'ro.build.date.utc': 'device_firmware_date',
            'ro.product.device': 'device_id'}
        for line in build_props.split('\n'):
            if not line.strip().startswith('#') and '=' in line:
                key, value = [s.strip() for s in line.split('=', 1)]
                if key in list(desired_props.keys()):
                    self._info[desired_props[key]] = value

        if self._info.get('device_id', '').lower() == 'flame':
            for prop in ['ro.boot.bootloader', 't2m.sw.version']:
                value = dm.shellCheckOutput(['getprop', prop])
                if value:
                    self._info['device_firmware_version_base'] = value
                    break

    def get_gaia_info(self, app_zip):
        tempdir = tempfile.mkdtemp()
        try:
            gaia_commit = os.path.join(tempdir, 'gaia_commit.txt')
            try:
                zip_file = zipfile.ZipFile(app_zip.name)
                with open(gaia_commit, 'w') as f:
                    f.write(zip_file.read('resources/gaia_commit.txt'))
            except zipfile.BadZipfile:
                self._logger.info('Unable to unzip application.zip, falling '
                                  'back to system unzip')
                from subprocess import call
                call(['unzip', '-j', app_zip.name, 'resources/gaia_commit.txt',
                      '-d', tempdir])

            with open(gaia_commit) as f:
                changeset, date = f.read().splitlines()
                self._info['gaia_changeset'] = re.match(
                    '^\w{40}$', changeset) and changeset or None
                self._info['gaia_date'] = date
        except KeyError:
                self._logger.warning(
                    'Unable to find resources/gaia_commit.txt in '
                    'application.zip')

    def get_gecko_info(self, path):
        for type, section in INI_DATA_MAPPING:
            config_file = os.path.join(path, "%s.ini" % type)
            if os.path.exists(config_file):
                self._parse_ini_file(open(config_file), type, section)
            else:
                self._logger.warning('Unable to find %s' % config_file)

    def _parse_ini_file(self, fp, type, section):
        config = configparser.RawConfigParser()
        config.readfp(fp)
        name_map = {'codename': 'display_name',
                    'milestone': 'version',
                    'sourcerepository': 'repository',
                    'sourcestamp': 'changeset'}
        for key, value in config.items(section):
            name = name_map.get(key, key).lower()
            self._info['%s_%s' % (type, name)] = config.has_option(
                section, key) and config.get(section, key) or None

        if not self._info.get('application_display_name'):
            self._info['application_display_name'] = \
                self._info.get('application_name')

