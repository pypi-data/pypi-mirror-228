import logging
import types
import weakref
import copy

from collections.abc import Iterable
from collections.abc import MutableMapping
from pyats.topology.credentials import Credentials
from pyats.topology.device import Device as pyATSDevice

from genie.metaparser.util import merge_dict
from ..base.interface import BaseInterface
from ..base.link import Link
from ..base.device import Device
from ..base.testbed import Testbed

logger = logging.getLogger(__name__)


class Converter(object):
    """ Converter class

    `Converter` class convert pyats base objects (Testbed, Device, Link,
    Interface) into Genie base objects.
    """

    @classmethod
    def reparent_credentials(self, obj_with_credentials, new_parent):
        """ class method to reassign the parent of contained credentials
        """
        if getattr(obj_with_credentials, 'credentials', None) is not None \
                and isinstance(obj_with_credentials.credentials, Credentials):
            obj_with_credentials.credentials.parent = new_parent
        if isinstance(obj_with_credentials, MutableMapping):
            for item in obj_with_credentials:
                self.reparent_credentials(
                    obj_with_credentials[item], new_parent)


    @classmethod
    def convert_tb(self, pyats_testbed):
        """ class method to convert pyats testbed obj into Genie Testbed obj

        API converts pyats testbed obj and all inner objects into Genie objs

        Args:
            pyats_testbed (`Testbed`): pyats Testbed obj

        Returns:
                a Genie `Testbed` object

        Examples:
            get the testbed yaml file

            >>> test_path = os.path.dirname(os.path.dirname(
            ...             os.path.abspath(__file__)))
            >>> yaml = os.path.join(test_path, 'testscript/etc/ott-genie.yaml')

            load the yaml file and create ats testbed obj

            >>> from pyats.topology import loader
            >>> tb = loader.load(yaml)

            convert ats Testbed obj into Genie Testbed obj

            >>> genie_tb = Converter.convert_tb(tb)

            <genie.conf.base.testbed.Testbed object at 0xf6b5a06c>
        """
        # Instanciate the devices/interfaces/links
        # Create a testbed object

        testbed = Testbed(name=pyats_testbed.name)

        for name, obj in pyats_testbed.devices.items():
            # Create a new device
            self.convert_device(obj, testbed)

        for pyats_link in pyats_testbed.links:
            if pyats_link.name not in testbed.links:
                if pyats_link.name == 'netboot':
                    continue

                # Convert pyATS link to Genie link
                link = self.convert_link(pyats_link, testbed)

                if link != pyats_link:
                    # Add the interface to the link
                    for pyats_intf in pyats_link.interfaces:
                        dev = testbed.devices[pyats_intf.device.name]
                        link.connect_interface(dev.interfaces[pyats_intf.name])

        for item in pyats_testbed.__dict__:
            if isinstance(getattr(pyats_testbed, item), types.FunctionType):
                setattr(testbed, item, getattr(pyats_testbed, item))
            if isinstance(item, Iterable):
                # Handling the case where the item value is a dictionary
                if not isinstance(getattr(pyats_testbed, item), dict):
                    setattr(testbed, item, getattr(pyats_testbed, item))
                else:
                    if item in testbed.__dict__:
                        merge_dict(getattr(testbed, item),
                            getattr(pyats_testbed, item),
                            ignore_update=True)
                    else:
                        setattr(testbed, item, getattr(pyats_testbed, item))

            if item == 'servers':
                self.reparent_credentials(getattr(testbed, item), testbed)


        return testbed

    @classmethod
    def convert_device(self, pyats_device, testbed):
        """ class method to convert pyats Device obj into genie Device obj

        API converts pyats device obj and all inner objects into genie objs

        Args:
            pyats_device (`Device`): pyats Device obj
            testbed (`Testbed`): Genie converted Testbed

        Returns:
                a genie `Device` object

        Examples:
            get the testbed yaml file

            >>> test_path = os.path.dirname(os.path.dirname(
            ...             os.path.abspath(__file__)))
            >>> yaml = os.path.join(test_path, 'testscript/etc/ott-genie.yaml')

            load the yaml file and create ats testbed obj

            >>> from pyats.topology import loader
            >>> tb = loader.load(yaml)

            get an ats Device obj

            >>> device = tb.devices['PE1']

            convert ats Device obj into genie Device obj

            >>> genie_device = Converter.convert_device(device, genieTestbed)

            <genie.conf.base.device.Device object at 0xf3b5a06d>
        """

        # Create genie Device object
        if hasattr(pyats_device, 'os'):
            kwargs_ = {'os':pyats_device.os}
        else:
            kwargs_ = {}

        # if match one below condition, device conversion will be skipped
        # - not pyATS or Genie Device class
        explicit_class = None
        if hasattr(pyats_device.testbed, 'raw_config'):
            explicit_class = pyats_device.testbed.raw_config['devices'][pyats_device.name].get('class')
        if explicit_class:
            logger.debug(
                f"Convert to Genie Device for {pyats_device.name} is skipped since deviceclass {explicit_class} is explicitly given."
            )
            pyats_device.testbed = testbed
            return pyats_device

        device = Device(name=pyats_device.name,
                        aliases=[pyats_device.alias],
                        testbed=testbed,
                        **kwargs_)

        for item in pyats_device.__dict__:
            if item == 'connectionmgr':
                getattr(device, item).__dict__ = \
                    copy.copy(getattr(pyats_device, item).__dict__)
                getattr(device, item).__dict__['__device__'] = \
                    weakref.ref(device)
                if pyats_device.connectionmgr.connections.get('default'):
                    device.connectionmgr.connections['cli'] = pyats_device.connectionmgr.connections['default']

                continue

            # Interfaces have been already added to the device,
            # otherwise will get DuplicateInterfaceError
            # __testbed__ is the pyats testbed and we don't want to override
            # genie device one with the pyats one.
            exclude = ['interfaces', '__testbed__']
            if item in exclude:
                continue
            if isinstance(getattr(pyats_device, item), types.FunctionType):
                setattr(device, item, getattr(pyats_device, item))
            if isinstance(getattr(pyats_device, item), Credentials):
                setattr(device, item, getattr(pyats_device, item))
                setattr(getattr(device, item), 'parent', testbed)
                continue
            if isinstance(item, Iterable):
                # Handling the case where the item value is a dictionary
                if not isinstance(getattr(pyats_device, item), dict):
                    setattr(device, item, getattr(pyats_device, item))
                else:
                    if item in device.__dict__:
                        merge_dict(getattr(device, item),
                            getattr(pyats_device, item),
                            ignore_update=False)
                    else:
                        setattr(device, item, getattr(pyats_device, item))
            if item == 'connections':
                self.reparent_credentials(getattr(device, item), device)


        # Loop through all interfaces of pyats_device
        # Convert them and add them to genie_devce
        for obj in pyats_device.interfaces.values():
            self.convert_interface(obj, device)

        # Check if custom abstraction OS is there, else provide default
        if not getattr(device.custom, 'abstraction', None) or \
           'order' not in device.custom.abstraction.keys():
            # Set default
            device.custom.setdefault('abstraction', {})['order'] = ['os', 'platform', 'model']

        return device

    @classmethod
    def convert_interface(self, pyats_interface, device):
        """ class method to convert pyats Interface obj into genie Interface
        obj

        API converts pyats interface obj into genie interface  objs

        Args:
            pyats_interface (`Interface`): pyats Interface obj
            device (`Device`): Genie converted Device

        Returns:
                a genie `Interface` object

        Examples:
            get the testbed yaml file

            >>> test_path = os.path.dirname(os.path.dirname(
            ...             os.path.abspath(__file__)))
            >>> yaml = os.path.join(test_path, 'testscript/etc/ott-genie.yaml')

            load the yaml file and create ats testbed obj

            >>> from pyats.topology import loader
            >>> tb = loader.load(yaml)

            get an ats Device obj

            >>> device = tb.devices['PE1']

            get an ats Interface obj

            >>> intf =  device.interfaces['Ethernet4/45']

            convert ats Interface obj into genie Interface obj

            >>> genie_interface = Converter.convert_interface(intf,
            ... genieDevice)

            <genie.conf.base.interface.EthernetInterface object at 0xf2b3a06e>
        """

        if pyats_interface.__class__.__module__.split('.')[0] not in ['pyats', 'genie']:
            pyats_interface.device = device
            return pyats_interface

        # Create Genie Interface object
        # Which get attached to device via Genie device object
        if hasattr(pyats_interface, 'tunnel_mode'):
            interface = BaseInterface(aliases=[pyats_interface.alias],
                                      name=pyats_interface.name,
                                      type=pyats_interface.type,
                                      device=device,
                                      tunnel_mode=pyats_interface.tunnel_mode)
        else:
            interface = BaseInterface(aliases=[pyats_interface.alias],
                                      name=pyats_interface.name,
                                      type=pyats_interface.type,
                                      device=device)

        for item in pyats_interface.__dict__:
            if item == 'ipv4' or item == 'ipv6':
                setattr(interface, item, getattr(pyats_interface, item))
            if isinstance(getattr(pyats_interface, item), types.FunctionType):
                setattr(interface, item, getattr(pyats_interface, item))
            if isinstance(item, Iterable):
                # Handling the case where the item value is a dictionary
                if not isinstance(getattr(pyats_interface, item), dict):
                    setattr(interface, item, getattr(pyats_interface, item))
                else:
                    if item in interface.__dict__:
                        merge_dict(getattr(interface, item),
                            getattr(pyats_interface, item),
                            ignore_update=False)
                    else:
                        setattr(interface, item, getattr(pyats_interface, item))

        # interface.device needs to be the Genie one. override has been done
        # in the above for loop so we needed to retrieve it back.
        interface.device = device

        return interface

    @classmethod
    def convert_link(self, pyats_link, testbed):
        """ class method to convert pyats Link obj into genie Link obj

        API converts pyats link obj into genie link  objs

        Args:
            pyats_link (`Link`): pyats Link obj
            testbed (`Testbed`): Genie converted Testbed

        Returns:
                a genie `Link` object

        Examples:
            get the testbed yaml file

            >>> test_path = os.path.dirname(os.path.dirname(
            ...             os.path.abspath(__file__)))
            >>> yaml = os.path.join(test_path, 'testscript/etc/ott-genie.yaml')

            load the yaml file and create ats testbed obj

            >>> from pyats.topology import loader
            >>> tb = loader.load(yaml)

            get an ats Device obj

            >>> device = tb.devices['PE1']

            get an ats Interface obj

            >>> intf =  device.interfaces['Ethernet4/45']

            get an ats Link obj

            >>> link =  intf.link

            convert ats Link obj into genie Link obj
            >>> genie_link = Converter.convert_link(link, genieTestbed)

            <genie.conf.link.Link object at 0xf4b3f06r>
        """

        if pyats_link.__class__.__module__.split('.')[0] not in ['pyats', 'genie']:
            pyats_link.testbed = testbed
            return pyats_link

        # Create new link
        # Which get attached to testbed via genie testbed object
        link = Link(name=pyats_link.name,
                    aliases=[pyats_link.alias],
                    testbed=testbed)

        for item in pyats_link.__dict__:
            if item == 'interfaces':
                # link will be connected later to the interface so no need to
                # do it twice, otherwise we will get the
                # DuplicateInterfaceConnectionError
                continue
            if isinstance(getattr(pyats_link, item), types.FunctionType):
                setattr(link, item, getattr(pyats_link, item))
            if isinstance(item, Iterable):
                # Handling the case where the item value is a dictionary
                if not isinstance(getattr(pyats_link, item), dict):
                    setattr(link, item, getattr(pyats_link, item))
                else:
                    if item in link.__dict__:
                        merge_dict(getattr(link, item),
                            getattr(pyats_link, item),
                            ignore_update=False)
                    else:
                        setattr(link, item, getattr(pyats_link, item))

        return link
