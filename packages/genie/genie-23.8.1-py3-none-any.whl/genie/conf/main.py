import os
import logging
from enum import Enum
from pyats.topology import loader
from genie.conf.base import Device
from .utils.converter import Converter
from pyats.topology.testbed import Testbed
from pyats.topology.credentials import Credentials
from genie.conf.base import Testbed as GenieTestbed
from genie.metaparser.util.schemaengine import Schema, Any, Optional

logger = logging.getLogger(__name__)

QUICK_TB_SCHEMA = {
    'devices': {
        Any(): {
            'os': str,
            'protocol': str,
            'ip': str,
            Optional('port'): int,
            'username': str,
            'password': str,
            Optional('enable_password'): str
        }
    }
}

class Genie(object):
    """ `Genie` entry class

    `Genie` entry functionality. Allows to automatically instantiate `Genie`
    Testbed from pyATS testbed.
    """

    class Context(Enum):
        cli = 'cli'
        yang = 'yang'
        xml = 'xml'

        def __str__(self):
            return str(self.value)


    # Class variable to retrieve testbed
    testbed = None
    context = Context.cli

    @classmethod
    def init(cls, testbed):
        """ initialize the Genie base objects

        Class method that converts pyATS testbed object, including
        devices, interfaces and link, to `Genie` objects.

        Args:
            testbed (`file/pyAts Testbed`): Path to Yaml file or pyATS Testbed

        Raises:
            TypeError when wrong Testbed is passed


        Returns:
                `Genie` `Testbed` object

        Examples:

            >>> from genie.conf import Genie
            # Figure out current location
            >>> test_path = os.path.dirname(
                                    os.path.dirname(os.path.abspath(__file__)))
            # Current location + relative path to yaml file
            >>> yaml = os.path.join(test_path, 'testscript/etc/ott-genie.yaml')
            # Store Genie testbed into genie_tb variable
            >>> genie_tb = Genie.init(testbed=yaml)
            <genie.conf.base.testbed.Testbed object at 0xf6b5a06c>

            Assuming there is a pyATS Testbed object

            >>> genie_tb = Genie.init(testbed=pyats_testbed)
            <genie.conf.base.testbed.Testbed object at 0xf6b5a76c>

            Lastly, the testbed is stored as a class variable
            which can be used to retrieve Testbed at later time in
            other functions

            >>> Genie.testbed == genie_tb
            True

        """

        if isinstance(testbed, GenieTestbed):
            logger.debug('Testbed object {} is a genie testbed, '
                         'skipping conversion'.format(repr(testbed)))
            cls.testbed = testbed

        elif isinstance(testbed, Testbed):
            cls.testbed = Converter.convert_tb(testbed)

        elif cls.is_quick_tb(testbed):
            cls.testbed = cls.convert_quick_tb(testbed)

        else:
            cls.testbed = loader.load(testbed)

        return cls.testbed

    @classmethod
    def is_quick_tb(cls, testbed):
        """ Method to check if the 'testbed' is a quick-testbed as seen here:
        https://pubhub.devnetcloud.com/media/genie-docs/docs/cookbooks/genie.html#create-a-testbed-from-a-dictionary
        """
        if not isinstance(testbed, dict):
            return False

        try:
            Schema(QUICK_TB_SCHEMA).validate(testbed)
        except Exception as e:
            logger.debug('Testbed is not a quick-testbed. Error: {}'.format(e))
            return False

        return True

    @classmethod
    def convert_quick_tb(cls, testbed):
        tb = GenieTestbed(name='')
        for name, dev in testbed.get('devices', {}).items():
            try:
                tmp_device = dev.copy()
                os = tmp_device.pop('os')
                port = tmp_device.pop('port', None)
                # build the connection dict
                connections = {
                    'cli': {
                        'ip': tmp_device.pop('ip'),
                        'protocol': tmp_device.pop('protocol')}}

                if port:
                    connections['cli'].update({'port': int(port)})
                credentials = {
                    'default': {
                        'username': tmp_device.pop('username'),
                        'password': tmp_device.pop('password')},
                    'enable':{
                        'password': tmp_device.pop('enable_password', dev['password'])
                    }}
                device = Device(name=name,
                                os=os,
                                credentials=Credentials(credentials),
                                connections=connections,
                                **tmp_device)
                device.custom.setdefault('abstraction', {})['order'] = ['os', 'platform', 'model']
            except KeyError as e:
                raise KeyError('Missing required key {k} for device {d}'.format(k=str(e),
                                                                                d=name))
            tb.add_device(device)

        return tb
