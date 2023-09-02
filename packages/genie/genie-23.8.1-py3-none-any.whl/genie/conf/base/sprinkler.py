from netaddr import mac_cisco, EUI, core
from ipaddress import ip_network, IPv4Network, IPv4Address, ip_address,\
    IPv4Interface, IPv6Interface

from .decorator import log_it


class InterfaceName(object):
    ''' This class generates virtual interface name

    Allows to get interface name on a particular device,
    If the interface is already present then it will raise an exception.

    Args:
        device : device object where we need to create the interfaces
        name : Virtual Interface name which has to be created
        iterable : list or range of virtual interfaces that has to be created

    Example :

        >>> from genie.conf.base.sprinkler import InterfaceName
        >>> from genie.libs.conf.interface.nxos import LoopbackInterface,

        >>> loopback = InterfaceName.loopback(device=dev, name='loopback',
                                              iterable=[0])
        >>> loopback
        'loopback0'
        >>> intf = LoopbackInterface(device=dev, name = 'loopback1')
        >>> loopback = InterfaceName.loopback(device=dev, name='loopback',
                                              iterable=[2])
        *** ValueError: No name available for loopback on my_device
    '''

    @classmethod
    def loopback(cls, device, name, iterable=range(0, 1024)):
        '''Generates loopback interfaces for a particular device

        Example :

            >>> from genie.conf.base.sprinkler import InterfaceName
            >>> from genie.libs.conf.interface.nxos import \
            ... LoopbackInterface
            >>> loopback = InterfaceName.loopback(device=dev, name='loopback',
                                                  iterable=[0])
            >>> loopback
            'loopback0'
            >>> intf = LoopbackInterface(device=dev, name = 'loopback1')
            >>> loopback = InterfaceName.loopback(device=dev, name='loopback',
                                                  iterable=[2])
            *** ValueError: No name available for loopback on my_device
        '''
        return cls._generate(device=device, name=name, iterable=iterable)

    @classmethod
    def vlan(cls, device, name, iterable=range(0, 4095)):
        '''Generate vlan interfaces for a particular device

        Example :

            >>> from genie.conf.base.sprinkler import InterfaceName
            >>> from genie.libs.conf.interface.nxos import VlanInterface
            >>> vlan = InterfaceName.vlan(device=dev, name='vlan',
            ... iterable=[0])
            >>> vlan
            'vlan0'
            >>> intf = VlanInterface(device=dev, name = 'Vlan1')
            >>> vlan = InterfaceName.vlan(device=dev, name='vlan',
            ... iterable=[2])
            *** ValueError: No name available for vlan on my_device
        '''
        return cls._generate(device=device, name=name, iterable=iterable)

    @classmethod
    def port_channel(cls, device, name, iterable=range(0, 4097)):
        '''Generates port-channel interfaces for a particular device

        Example :

            >>> from genie.conf.base.sprinkler import InterfaceName
            >>> from genie.libs.conf.interface.nxos import
                PortchannelInterface

            >>> po = InterfaceName.port_channel(device=dev,
            ... name='port-channel', iterable=[0])
            >>> po
            'port-channel0'
            >>> intf = PortchannelInterface(device=dev, name = 'port-channel1')
            >>> po = InterfaceName.port_channel(device=dev,
            ... name='port-channel', iterable=[2])
            *** ValueError: No name available for port-channel on my_device
        '''
        return cls._generate(device=device, name=name, iterable=iterable)

    @classmethod
    def _generate(cls, device, name, iterable):
        # For values, verify if it is already on the device.
        # If not, we got it!
        # It could be improve for speed if needed
        for number in iterable:
            ret_name = '{name}{number}'.format(name=name, number=number)
            if ret_name not in device.interfaces:
                return ret_name
        raise ValueError('No name available for {name} on '
                         '{device}'.format(name=name,
                                           device=device.name))


class IpUtils:
    '''This class has a function to convert an IP address to a MAC address.

       Feature  is added to convert ip multicast address to the destination
       MAC equivalent as well.

    Example :

        >>> from genie.conf.base.sprinkler import IpUtils

        >>> mac = IpUtils.ip_to_mac(host_addr='224.234.23.45')
        >>> mac
        0100.5e6a.172d

        >>> mac = IpUtils.ip_to_mac(host_addr='10.234.23.45')
        >>> mac
        0000.0aea.172d
    '''

    def __init__(self,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def ip_to_mac(cls, host_addr):
        '''This function converts an IP address to a MAC address.  This would
          be useful for such things as creating MAC addresses for the
          Ethernet cards.

        Args:
            host_addr: ip address which needs to be converted to mac

        Returns:
          MAC address.
        '''

        host_addr = ip_address(host_addr)
        if isinstance(host_addr, IPv4Address):

            # check if the given ip address is multicast address
            if host_addr.is_multicast == True:
                mac = EUI(
                    0x01005e000000
                    + (int(host_addr) & 0x007FFFFF))

            # if the given ip address is unicast address
            else:
                mac = EUI(int(host_addr))

        else:

            # check if the given ip address is multicast address
            if host_addr.is_multicast == True:
                mac = EUI(
                    0x333300000000
                    + (int(host_addr) & 0xFFFFFFFF))

            # if the given ip address is unicast address
            else:
                # Works best for link-local addresses:
                # 'fe80:0000:0000:0000:be5f:f4ff:fe19:ad18' -> 'be5f.f419.ad18'
                mac = EUI(
                    (int(host_addr) & 0x00FFFFFF)
                    | ((int(host_addr) >> 8) & 0xFFFFFF000000)
                )
                # TODO what about the global/local bit?
                # TODO return EUI-64?

        mac.dialect = mac_cisco
        return mac


class Ip(object):

    '''This class is an ip generator, for getting the next network, next host

    Example :

        >>> from genie.conf.base.sprinkler import Ip
        >>> from ipaddress import ip_network, IPv4Network, IPv4Address,
            ip_address, IPv4Interface

        >>> ipv4 = Ip(network="10.1.1.0",mask='24')
        >>> ipv4.next_network()
        >>> ipv4
        '10.1.2.0'
        >>> ipv4.next_ip()
        >>> ipv4
        '10.1.2.1
        >>> ipv4.reset()
        >>> ipv4
        '10.1.1.0/24'
    '''

    def __init__(self, network='1.1.1.0', mask='24'):
        self._root_network = network
        self._root_mask = mask

        self.reset()

    def _networks(self, network):

        '''This functions increments  the network or the host on
        the specified ipv4 address based on the netmask provided

        Args:
            network: ipv4 network address
            mask: ipv4 network mask

        Returns:
          Increments address in IPv4 format, or an error is thrown
          if not supported.
        '''

        mask = network.netmask.compressed
        net_ip = network.network_address
        net_ip_compressed = network.network_address.compressed
        net_ip_octet = net_ip_compressed.split(".")
        net_mask_octet = mask.split(".")
        count = 0
        diff = None
        cidr = 0
        for i in net_mask_octet:
            if int(i) < 255 and int(i) != 0:
                diff = 256 - int(i)
                cidr = 1
                break
            count += 1

        if cidr:
            for j in range(0, 255, diff):
                net_ip_octet[count] = int(net_ip_octet[count]) + diff
                if (int(net_ip_octet[count]) < 255):
                    network_ip = '.'.join(str(k) for k in net_ip_octet)
                    yield ip_network('{n}/{m}'.format(n=network_ip,
                                                      m=network.prefixlen))
        else:
            count = 0
            for i in net_mask_octet:
                if int(i) == 0:
                    diff = 1
                    break
                count += 1
            if int(net_mask_octet[3]) == 255:
                raise ValueError("Subnet mask cannot be /32 for network")

            for abc in range(0, 255, diff):
                net_ip_octet[count - 1] = int(net_ip_octet[count - 1]) + diff
                if (int(net_ip_octet[count - 1]) < 255):
                    network_ip = '.'.join(str(k) for k in net_ip_octet)
                    yield ip_network('{n}/{m}'.format(n=network_ip,
                                                      m=network.prefixlen))

    @log_it
    def reset(self):
        '''Resets the ipv4 address.

            Examples:

            >>> from genie.conf.base.sprinkler import Ip
            >>> from ipaddress import ip_network, IPv4Network, IPv4Address,
                ip_address, IPv4Interface

            >>> ipv4 = Ip(network="10.1.1.0",mask='24')
            >>> ipv4.next_network()
            >>> ipv4
            '10.1.2.0'
            >>> ipv4.reset()
            >>> ipv4
            '10.1.1.0/24'

        Returns: Ipv4 address with mask.

        '''
        # Resets the ipv4 address to which it was set earlier
        self.network = ip_network('{n}/{m}'.format(n=self._root_network,
                                                   m=self._root_mask))

        self.hosts = self.network.hosts()
        self._generator = self._networks(self.network)

    @log_it
    def next_network(self):
        '''Gives the next ipv4 network of the given network

        Examples:

            >>> from genie.conf.base.sprinkler import Ip
            >>> from ipaddress import ip_network, IPv4Network, IPv4Address,
                ip_address, IPv4Interface

            >>> ipv4 = Ip(network="10.1.1.0",mask='24')
            >>> ipv4.next_network()
            >>> ipv4
            '10.1.2.0'

        Returns: Ipv4 network or Raises StopIteration Error if the
                 network exceeds the limit of the ipv4 subnetmask

        '''
        self.network = next(self._generator)
        self.hosts = self.network.hosts()

    @log_it
    def next_ip(self):
        '''Gives the next ipv4 address of the given network

        Examples:

            >>> from genie.conf.base.sprinkler import Ip
            >>> from ipaddress import ip_network, IPv4Network, IPv4Address,
                ip_address, IPv4Interface

            >>> ipv4 = Ip(network="10.1.1.0",mask='24')
            >>> ipv4.next_ip()
            >>> ipv4
            '10.1.2.1'

        Returns: Ipv4 address or Raises StopIteration Error if the
                 network exceeds the limit of the ipv4 subnetmask

        '''
        ip = next(self.hosts)
        return IPv4Interface('{ip}/{m}'.format(ip=ip,
                                               m=self.network.prefixlen))


class Ipv6(object):

    '''This class is an ip generator, for getting the next network, next host

    Example :

        >>> from genie.conf.base.sprinkler import Ipv6
        >>> from ipaddress import ip_network, IPv4Network, IPv4Address,
            ip_address, IPv4Interface

        >>> ipv6 = Ipv6(network="2001:db00::",mask='64')
        >>> ipv6.next_network()
        >>> ipv6
        '2001:db00:0:1::'
        >>> ipv6
        >>> ipv6.next_ip()
        '2001:db00:0:1::1'
        >>> ipv6.reset()
        '2001:db00::'
    '''

    def __init__(self, network='1::0', mask='64'):
        self._root_network = network
        self._root_mask = mask

        self.reset()

    def _networks(self, network):

        '''This functions increments  the network or the host on
        the specified ipv6 address based on the netmask provided

        Args:
            network: ipv6 network address
            mask: ipv6 subnet mask

        Returns:
          Increments address in IPv6 format, or an error is thrown
          if not supported.
        '''

        mask = network.netmask.exploded
        net_ip = network.network_address
        net_ip_exploded = network.network_address.exploded
        net_ip_octet = net_ip_exploded.split(":")
        net_mask_octet = mask.split(":")
        count = 0
        diff = None
        cidr = 0

        for i in net_mask_octet:
            a = eval('0x' + i)
            if int(a) < int(0xffff) and int(a) != 0:
                diff = Ipv6.diff_hex(hex(0xffff), hex(a))
                cidr = 1
                break
            count += 1

        if cidr:
            subnet_corr = 1
            for j in range(0, int(0xffff), int(eval(diff))):
                net_ip_octet[count] = Ipv6.add_hex(net_ip_octet[count], diff)
                net_ip_octet[count] = Ipv6.add_hex(net_ip_octet[count],
                                                   hex(subnet_corr))

                if (int(eval(net_ip_octet[count])) < int(0xffff)):
                    net_ip_octet[count] = hex(eval(net_ip_octet[count])).\
                        replace('0x', '')
                    network_ip = ':'.join(str(k) for k in net_ip_octet)
                    yield ip_network('{n}/{m}'.format(n=network_ip,
                                                      m=network.prefixlen))
        else:
            count = 0
            for i in net_mask_octet:
                a = eval('0x' + i)
                if int(a) == int(0):
                    diff = 1
                    break
                count += 1
            if str(net_mask_octet[7]) == 'ffff':
                raise ValueError("Subnet mask cannot be /128 for ipv6 network")
            for abc in range(0, int(0xffff), diff):
                net_ip_octet[count - 1] = Ipv6.add_hex(net_ip_octet[count - 1],
                                                       hex(diff))

                if (int(eval(net_ip_octet[count-1])) < int(0xffff)):
                    net_ip_octet[count-1] = hex(eval(net_ip_octet[count-1])).\
                        replace('0x', '')
                    network_ip = ':'.join(str(k) for k in net_ip_octet)
                    yield ip_network('{n}/{m}'.format(n=network_ip,
                                                      m=network.prefixlen))

    @log_it
    def add_hex(hex1, hex2):
        '''Adds 2 hexadecimal number

        Args:
            hex1: first hexadecimal number
            hex2: second hexadecimal number

        Returns: hexadecimal number which is sum of hex1 and hex2

        '''
        return hex(int(hex1, 16) + int(hex2, 16))

    @log_it
    def diff_hex(hex1, hex2):
        '''Subtracts 2 hexadecimal number

        Args:
            hex1: first hexadecimal number
            hex2: second hexadecimal number

        Returns: hexadecimal number which is a difference of hex1 and hex2

        '''
        return hex(int(hex1, 16) - int(hex2, 16))

    @log_it
    def reset(self):
        '''Resets the ipv6 address

        Example :

            >>> from genie.conf.base.sprinkler import Ipv6
            >>> from ipaddress import ip_network, IPv4Network, IPv4Address,
                ip_address, IPv4Interface

            >>> ipv6 = Ipv6(network="2001:db00::",mask='64')
            >>> ipv6.next_network()
            >>> ipv6
            '2001:db00:0:1::'
            >>> ipv6
            >>> ipv6.reset()
            >>>ipv6.network.network_address.compressed
            '2001:db00::'

        Returns: Ipv6 address

        '''

        self.network = ip_network('{n}/{m}'.format(n=self._root_network,
                                                   m=self._root_mask))

        self.hosts = self.network.hosts()
        self._generator = self._networks(self.network)

    @log_it
    def next_network(self):
        '''Gives the next ipv4 network of the given network

        Example :

            >>> from genie.conf.base.sprinkler import Ipv6
            >>> from ipaddress import ip_network, IPv4Network, IPv4Address,
                ip_address, IPv4Interface

            >>> ipv6 = Ipv6(network="2001:db00::",mask='64')
            >>> ipv6.next_network()
            >>> ipv6.network.network_address.compressed
            '2001:db00:0:1::'

        Returns:Ipv6 network or Raises StopIteration Error if the
                 network exceeds the limit of the ipv6 subnetmask

        '''
        self.network = next(self._generator)
        self.hosts = self.network.hosts()

    @log_it
    def next_ip(self):
        '''Gives the next ipv6 address of the given network

        Examples:

            >>> from genie.conf.base.sprinkler import Ipv6
            >>> from ipaddress import ip_network, IPv4Network, IPv4Address,
                ip_address, IPv4Interface

            >>> ipv6 = Ipv6(network="2001:db00::",mask='64')
            >>> ipv6.next_network()
            >>> ipv6
            '2001:db00:0:1::'
            >>> ipv6
            >>> ipv6.next_ip()
            >>> ipv6..ip.compressed
            '2001:db00::1'

        Returns: Ipv6 address or Raises StopIteration Error if the
                 network exceeds the limit of the ipv6 subnetmask

        '''
        ip = next(self.hosts)
        return IPv6Interface('{ip}/{m}'.format(ip=ip,
                                               m=self.network.prefixlen))
