import copy
import math
import builtins
from collections import OrderedDict
import collections.abc
from collections.abc import Iterable
from ipaddress import IPv4Address, IPv4Interface, IPv4Network
from ipaddress import IPv6Address, IPv6Interface, IPv6Network
from ipaddress import ip_address, ip_interface, ip_network
import netaddr
import functools

from pyats.datastructures.logic import BaseLogic
from genie.utils.cisco_collections import UserRange
from genie.utils import Dq

from .decorator import log_it


def prune_if(data, val_func):
    """
    data: JSON/YAML data (arbitrarily nested dicts, lists, etc)

    val_func: boolean function which is called on dictionary values, list
    elements and set elements. If val_func evaluates to True for a value
    then the value is deleted
    """
    if isinstance(data, collections.abc.Mapping):
        for k, v in list(data.items()):
            if val_func(v):
                del data[k]
        for v in data.values():
            prune_if(v, val_func)
    elif isinstance(data, collections.abc.MutableSequence):
        if len(data) == 1 and data[0] == data:
            if val_func(data[0]):
                data[:] = []
            # safeguard to not recurse infinitely
            # shouldnt happen but a single character string
            # for example is equal to its first element
            return

        data[:] = filter(lambda x: not val_func(x), data)
        for d in data:
            prune_if(d, val_func)
    elif isinstance(data, collections.abc.Set):
        if len(data) == 1 and list(data)[0] == data:
            if val_func(list(data)[0]):
                data.pop()
            # safeguard to not recurse infinitely
            return

        for d in list(data):
            if val_func(d):
                data.remove(d)
        for d in data:
            prune_if(d, val_func)


def _dict_to_string(stuff):
    ret = []
    for key, value in stuff.items():
        ret.append(key)
        ret.extend(_dict_to_string(value))
    return ret


def _merge_dict(a, b, path=None):
    """
    merges b into a
    """
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                _merge_dict(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                # same leaf value
                pass
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


def organize_dict(config, spaces=0):

    # Take copy of dict
    it_dict = copy.copy(config)

    for key, value in it_dict.items():
        config[key] = organize(value)
    return config


def organize(config, spaces=0, _infra=False):
    '''Remove duplicate configuration for the same level'''

    # If given was a string, convert to list
    try:
        config = config.splitlines()
    except:
        pass

    ret_config = []
    level = OrderedDict()

    # Find all the lines of this level
    # And loops through them

    # If it is of spaces 0, then we need to gather all of them
    if spaces == 0:
        care = [line for line in config
                if len(line) - len(line.lstrip(' ')) == spaces]
    else:
        # only care about this specific group, so break when
        # removed from this group
        care = []
        for line in config:
            whitespace = len(line) - len(line.lstrip(' '))
            if whitespace == spaces:
                care.append(line)
            elif whitespace > spaces:
                continue
            else:
                break


    for i, current_line in enumerate(config):

        # Don't care about those lines
        if current_line not in care:
            continue

        # Verify the white spaces
        current_spaces = len(current_line) - len(current_line.lstrip(' '))

        # But verify if next line is also the same level
        # If it has more white space, then current_line is
        # a 'multilevel' header
        try:
            next_spaces = len(config[i + 1]) - len(config[i + 1].lstrip(' '))
        except IndexError:
            # No next line, so let's assume it is the same as current
            next_spaces = current_spaces

        if current_spaces == spaces and current_spaces >= next_spaces:
            # This now mean that they are the same level
            # Though make sure this line is not already part of this list
            if current_line not in level:
                # ret_config.append(current_line)
                level[current_line] = {}

        if current_spaces < next_spaces:
            # Then current is a 'multilevel' header!
            # But... it isn't that easy, as maybe it already exists in dict
            # So let's verify if it does
            if current_line in level:
                # it already exists! so do nothing
                pass
            else:
                # it doesnt, so create it
                #level[current_line] = []
                level[current_line] = OrderedDict()

            # Now we need to check those lines within this indedation
            # We know where those lines begins, but now where they end
            # TODO : Bring the don't care line here ~
            returns = organize(config[i + 1:], spaces=next_spaces, _infra=True)
            for key, item in returns.items():
                # If already exists, merge
                if key in level[current_line]:
                    _merge_dict(level[current_line][key], item)
                else:
                    level[current_line][key] = item

        # Less white spaces, so it means we are done with this indendation
        elif current_spaces > next_spaces:
            break

    if _infra:
        return level

    # Join level with ret_config
    ret_config = _dict_to_string(level)

    # Take this list and convert to string and return it
    return '\n'.join(ret_config)


class IPv4AddressRange(UserRange):

    @classmethod
    def item_to_int(cls, item):
        if not isinstance(item, IPv4Address):
            raise TypeError(item)
        return int(item)

    @classmethod
    def step_to_int(cls, step):
        if not isinstance(step, (IPv4Address, int)):
            raise TypeError(step)
        return int(step)

    @classmethod
    def int_to_item(cls, i):
        if not type(i) is int:
            raise TypeError(i)
        return IPv4Address(i)

    @classmethod
    def int_to_step(cls, i):
        if not type(i) is int:
            raise TypeError(i)
        return i


class IPv6AddressRange(UserRange):

    @classmethod
    def item_to_int(cls, item):
        if not isinstance(item, IPv6Address):
            raise TypeError(item)
        return int(item)

    @classmethod
    def step_to_int(cls, step):
        if not isinstance(step, (IPv6Address, int)):
            raise TypeError(step)
        return int(step)

    @classmethod
    def int_to_item(cls, i):
        if not type(i) is int:
            raise TypeError(i)
        return IPv6Address(i)

    @classmethod
    def int_to_step(cls, i):
        if not type(i) is int:
            raise TypeError(i)
        return i


class IPv4InterfaceRange(UserRange):
    '''Range of IPv4Interface items.

    See also:
        testbed.ipv4_cache (IPv4InterfaceCache)
    '''

    network = None

    def item_to_int(self, item):
        if isinstance(item, IPv4Interface):
            pass
        else:
            try:
                IPv4Address(item)
            except:
                pass
            else:
                # Should not be compatible with a unmasked address
                raise TypeError(item)
            item = IPv4Interface(item)
        return int(item.ip)

    @classmethod
    def step_to_int(cls, step):
        if not isinstance(step, int):
            raise TypeError(step)
        return int(step)

    def int_to_item(self, i):
        if not type(i) is int:
            raise TypeError(i)
        return IPv4Interface('{}/{}'.format(
            IPv4Address(i),
            self.network.prefixlen))

    @classmethod
    def int_to_step(cls, i):
        if not type(i) is int:
            raise TypeError(i)
        return i

    def _item_repr(self, item):
        return repr(str(item))

    def __init__(self, *args):
        if not args:
            raise TypeError(args)
        item = args[0]
        if not isinstance(item, IPv4Interface):
            try:
                IPv4Address(item)
            except:
                pass
            else:
                # Should not be compatible with a unmasked address
                raise TypeError(item)
            item = IPv4Interface(item)
        self.network = item.network
        super().__init__(*args)

    def __str__(self):
        if self.data.step == 1 and bool(self):
            return '{}-{}'.format(self[0].ip, self[-1])
        else:
            return repr(self)


class IPv6InterfaceRange(UserRange):
    '''Range of IPv6Interface items.

    See also:
        testbed.ipv6_cache (IPv6InterfaceCache)
    '''

    network = None

    def item_to_int(self, item):
        if isinstance(item, IPv6Interface):
            pass
        else:
            try:
                IPv6Address(item)
            except:
                pass
            else:
                # Should not be compatible with a unmasked address
                raise TypeError(item)
            item = IPv6Interface(item)
        return int(item.ip)

    @classmethod
    def step_to_int(cls, step):
        if not isinstance(step, int):
            raise TypeError(step)
        return int(step)

    def int_to_item(self, i):
        if not type(i) is int:
            raise TypeError(i)
        return IPv6Interface('{}/{}'.format(
            IPv6Address(i),
            self.network.prefixlen))

    @classmethod
    def int_to_step(cls, i):
        if not type(i) is int:
            raise TypeError(i)
        return i

    def _item_repr(self, item):
        return repr(str(item))

    def __init__(self, *args):
        if not args:
            raise TypeError(args)
        item = args[0]
        if not isinstance(item, IPv6Interface):
            try:
                IPv6Address(item)
            except:
                pass
            else:
                # Should not be compatible with a unmasked address
                raise TypeError(item)
            item = IPv6Interface(item)
        self.network = item.network
        super().__init__(*args)

    def __str__(self):
        if self.data.step == 1 and bool(self):
            return '{}-{}'.format(self[0].ip, self[-1])
        else:
            return repr(self)


class mac_cisco_colons(netaddr.mac_cisco):
    '''Custom EUI/MAC dialect: `aaaa:bbbb:cccc`'''
    word_sep = ':'


class eui64_cisco_colons(netaddr.eui64_cisco):
    '''Custom EUI/MAC dialect: `aaaa:bbbb:cccc:dddd`'''
    word_sep = ':'


class MAC(netaddr.EUI):
    '''MAC address class.

    Main difference from the `netaddr.EUI` class is that `MAC` formats using
    the 'cisco' dialects.

    Examples:

        >>> from genie.conf.base.utils import MAC
        >>> MAC('1.2.3')
        EUI('0001.0002.0003')
        >>> MAC('1:2:3')
        EUI('0001.0002.0003')
    '''

    def __init__(self, addr, version=None):
        super().__init__(addr, version=version)
        if self.version == 48:
            self.dialect = netaddr.mac_cisco
        elif self.version == 64:
            self.dialect = netaddr.eui64_cisco
        else:
            raise ValueError('unsupported EUI version %r' % (self.version,))

    def __format__(self, format_spec):
        '''Support for format specifications.

        Called by the `format()` built-in function (and by extension, the
        `str.format()` method) to produce a "formatted" string representation
        of a MAC object.

        Arguments:
            format_spec: Any of the applicable `mac_*` and `eui64_*` dialects
                from the `netaddr` module or this module, without the `mac_` or
                `eui64_` prefix. Default is 'cisco'.

        Examples:

            >>> mac = MAC('1.2.3')
            >>> '{}'.format(mac)
            '0001.0002.0003'
            >>> '{:cisco}'.format(mac)
            '0001.0002.0003'
            >>> '{:cisco_colons}'.format(mac)
            '0001:0002:0003'
            >>> '{:eui48}'.format(mac)
            '00-01-00-02-00-03'
            >>> '{:unix}'.format(mac)
            '0:1:0:2:0:3'
            >>> '{:unix_expanded}'.format(mac)
            '00:01:00:02:00:03'
            >>> '{:bare}'.format(mac)
            '000100020003'

        '''
        if not format_spec:
            format_spec = 'cisco'
        if self.version == 48:
            dialect = getattr(netaddr, 'mac_' + format_spec, None) \
                or globals().get('mac_' + format_spec, None)
        elif self.version == 64:
            dialect = getattr(netaddr, 'eui64_' + format_spec, None) \
                or globals().get('eui64_' + format_spec, None)
        else:
            raise ValueError('unsupported EUI version %r' % (self.version,))
        if dialect is not None:
            if dialect is self.dialect:
                return str(self)
            else:
                other = netaddr.EUI(self)
                other.dialect = dialect
                return str(other)
        raise ValueError('Invalid format specifier')


class MACRange(UserRange):
    '''Range of MAC items.

    See also:
        testbed.mac_cache (MACCache)
    '''

    @classmethod
    def item_to_int(cls, item):
        if not isinstance(item, (netaddr.EUI, int)):
            item = MAC(item)
        return int(item)

    @classmethod
    def step_to_int(cls, step):
        if not isinstance(step, (netaddr.EUI, int)):
            raise TypeError(step)
        return int(step)

    @classmethod
    def int_to_item(cls, i):
        if not type(i) is int:
            raise TypeError(i)
        return MAC(i)

    @classmethod
    def int_to_step(cls, i):
        if not type(i) is int:
            raise TypeError(i)
        return i

    def _item_repr(self, item):
        return repr(str(item))

    def __str__(self):
        if self.data.step == 1 and bool(self):
            return '{}-{}'.format(self[0], self[-1])
        else:
            return repr(self)


class IntCache(object):
    '''Generic integer cache.

    Helper class to manage a cache of "reserved" integers.
    '''

    reserved = None  # [range, ...]

    def __init__(self):
        '''Initialize the IntCache with nothing reserved.'''
        self.reserved = []
        super().__init__()

    def add(self, range):
        '''Add a range() of integers to the cache.

        Any overlaps/collisions with previously reserved ranges will be
        silently merged; It is not an error to add the same integers to the
        cache multiple times.
        '''
        range_ = range
        range = builtins.range
        # A specific range is requested.
        # Go through the reserved list to see where it fits and merge or
        # add, as needed.
        assert 0 <= range_.start < range_.stop
        done = False
        for i_res, res in enumerate(self.reserved):
            if range_.start <= res.stop and range_.stop >= res.start:
                # collision
                if range_.start < res.start:
                    self.reserved[i_res] = res = range(range_.start, res.stop)
                if range_.stop > res.stop:
                    i_res2 = i_res + 1
                    while i_res2 < len(self.reserved):
                        res2 = self.reserved[i_res2]
                        if range_.stop < res2.start:
                            # disjoint
                            break
                        # collision with next
                        self.reserved.pop(i_res2)
                        if res2.stop < range_.stop:
                            # no i_res2 += 1!
                            continue  # keep expanding...
                        if res2.stop > range_.stop:
                            # expand...
                            range_ = range(range_.start, res2.stop)
                        # "stop"'s match; Stop!
                        break
                    self.reserved[i_res] = res = range(res.start, range_.stop)
                done = True
                break
            elif range_.stop <= res.start:
                # before
                self.reserved.insert(i_res, range(range_.start, range_.stop))
                done = True
                break
        if not done:
            # after
            self.reserved.append(range_)

    def reserve(self, count, start=0, alignment_mask=0):
        '''Reserve an unspecified range of integers.

        Args:
            count: Number of consecutive integers to reserve.
            start: Optional lowest possible integer to reserve.
            alignment_mask: Optional mask to help reserve a range appropriate
                to represent unused IP networks such that this holds true:
                    >>> reserve(count, alignment_mask).start \\
                    ...     alignment_mask == 0

        Return:
            range object representing a previously unreserved integers.
        '''
        count = int(count)
        assert 1 <= count
        start = int(start)
        stop = start + count
        # An unused range is requested.
        # Find a hole in the reserved list and fill it.
        if not self.reserved:
            self.reserved.append(range(start, stop))
        else:
            for i_res, res in enumerate(self.reserved):
                if start < res.stop and stop > res.start:
                    # collision
                    start = ((res.stop-1) | alignment_mask) + 1
                    stop = start + count
                elif res.start >= stop:
                    self.reserved.insert(i_res, range(start, stop))
                    # TODO check collisions/merges
                    break
            else:
                if self.reserved[-1].stop <= start:
                    self.reserved.append(range(start, stop))
                    # TODO check collisions/merges
                else:
                    raise RuntimeError(
                        'Failed to reserve a range of {} starting from {}!'\
                        .format(count, start))
        return range(start, stop)


class IPv4InterfaceCache(object):
    '''Generic IPv4Interface cache.

    Helper class to manage a cache of "reserved" IPv4Interface objects.

    See also:
        testbed.ipv4_cache
    '''

    _cache = None  # IntCache

    def __init__(self, reserve_defaults=True):
        '''Initialize the IPv4InterfaceCache.

        Args:
            reserve_defaults: If True, a standard set of defaults ranges are
                reserved which are largely innapropriate for use in a test
                network.
        '''
        self._cache = IntCache()
        super().__init__()
        if reserve_defaults:
            self.reserve('0.0.0.0/8')  # reserved
            self.reserve('127.0.0.0/8')  # reserved-loopback
            self.reserve('224.0.0.0/4')  # reserved-multicast
            self.reserve('5.0.0.0/8')  # reserved-lab (Cisco)
            self.reserve('223.255.254.0/24')  # reserved-lab (Cisco)

    def reserve(self, ipv4=None, count=None, netmask=None, prefixlen=None,
                type=None, range_count=1):
        '''Reserve an unused IPv4Interface range.

        Args:
            ipv4: A specific address or network to reserve (accepts
                overlaps/collisions.)
            count: Number of addresses to reserve.
            netmask: Netmask to reserve (implicit count).
            prefixlen: Prefix length to reserve (implicit count).
            type: Type/class of address: 'A', 'B', 'C', 'X' (extended) or
                'local' (127.*/32)
            range_count: For future use.

        Return:
            IPv4InterfaceRange

        Examples:

            >>> r = IPv4InterfaceCache()
            >>> r.reserve(count=2)
            >>> r.reserve(prefixlen=24)
            >>> r.reserve(netmask='255.255.255.0')
            >>> r.reserve('1.2.3.4')
            >>> r.reserve('1.2.3.0/24')
            >>> r.reserve('1.2.3.0/255.255.255.255')
            >>> r.reserve(type='A')

            >>> for link in core_links:
            ...     ipv4_range = testbed.ipv4_cache.reserve(prefixlen=24)
            ...     ipv4_it = iter(ipv4_range)
            ...     for interface in link.interfaces:
            ...         interface.ipv4 = next(ipv4_it)

        '''

        type_ = type
        type = builtins.type
        assert range_count
        assigned = False
        # netmask -> prefixlen
        if netmask is not None:
            assert prefixlen is None
            prefixlen = IPv4Network(
                '0.0.0.0/{}'.format(IPv4Address(netmask))).prefixlen
        # type_ -> ipv4/prefixlen
        if type_ is not None:
            assert ipv4 is None
            if type_ == 'A':
                ipv4 = IPv4Address('0.0.0.0')
                if prefixlen is None:
                    prefixlen = 8
            elif type_ == 'B':
                ipv4 = IPv4Address('128.0.0.0')
                if prefixlen is None:
                    prefixlen = 16
            elif type_ == 'C':
                ipv4 = IPv4Address('192.0.0.0')
                if prefixlen is None:
                    prefixlen = 24
            elif type_ == 'X':
                ipv4 = IPv4Address('224.0.0.0')
                if prefixlen is None:
                    prefixlen = 24
            elif type_ == 'local':
                ipv4 = IPv4Address('127.0.0.0')
                if prefixlen is None:
                    prefixlen = 32
            else:
                raise ValueError(type_)
        # ipv4 -> ipv4/prefixlen
        elif ipv4 is not None:
            assert type_ is None
            assert range_count == 1
            assigned = True
            try:
                ipv4 = IPv4Address(ipv4)
            except ValueError:
                ipv4 = IPv4Interface(ipv4)
            if type(ipv4) is IPv4Address:
                if prefixlen is None:
                    prefixlen = 32
            elif type(ipv4) is IPv4Interface:
                assert netmask is None
                assert prefixlen is None
                prefixlen = ipv4.network.prefixlen
                ipv4 = ipv4.ip

        # count|prefixlen -> bits_req, prefixlen, [tot_]ip_count, n_ip_mask
        if count is not None:
            assert not assigned
            # +2: Account for .0 and .255
            count = int(count)
            assert 1 <= count < (0xFFFFFFFF-2)
            # NOT (count + 2 - 1).bit_length()
            bits_req = math.ceil(math.log2(count + 2))
            prefixlen = 32 - bits_req
        elif prefixlen is not None:
            assert 1 <= prefixlen <= 32
            bits_req = 32 - prefixlen
        ip_count = 1 << bits_req
        tot_ip_count = ip_count * range_count
        n_ip_mask = (0xFFFFFFFF << bits_req) & 0xFFFFFFFF
        inv_n_ip_mask = n_ip_mask ^ 0xFFFFFFFF

        if assigned:
            # A specific range is requested.
            # Go through the reserved list to see where it fits and merge or
            # add, as needed.
            n_ip_from = int(ipv4) & n_ip_mask
            res = range(n_ip_from, n_ip_from + tot_ip_count)
            self._cache.add(res)

        else:
            # An unused range is requested.
            # Find a hole in the reserved list and fill it.
            if ipv4 is not None:
                min_n_ip_from = int(ipv4)
            else:
                if prefixlen >= 21:
                    min_n_ip_from = 0xC0000000  # 1100 pfx 21-32
                elif prefixlen >= 14:
                    min_n_ip_from = 0x80000000  # 1000 pfx 14-20
                else:
                    min_n_ip_from = 0x00000000  # 0000 pfx 7-13
                # min_n_ip_from = 0xE0000000  # 1110 reserved

            n_ip_from = min_n_ip_from
            res = self._cache.reserve(start=min_n_ip_from, count=tot_ip_count,
                                      alignment_mask=inv_n_ip_mask)
            n_ip_from = res.start

        # No post-transformation

        if bits_req > 1:
            n_ip_from = n_ip_from + 1  # .1
            if count is not None:
                ip_count = count
            else:
                ip_count = ip_count - 2  # full range except .0 and .255

        if assigned:
            start = IPv4Interface('{}/{}'.format(ipv4, prefixlen))
        else:
            start = IPv4Interface('{}/{}'.format(IPv4Address(n_ip_from),
                                                 prefixlen))

        return IPv4InterfaceRange(start, int(start.ip) + ip_count)


class IPv6InterfaceCache(object):
    '''Generic IPv6Interface cache.

    Helper class to manage a cache of "reserved" IPv6Interface objects.

    See also:
        testbed.ipv6_cache
    '''

    _cache = None  # IntCache

    def __init__(self, reserve_defaults=True):
        '''Initialize the IPv6InterfaceCache.

        Args:
            reserve_defaults: If True, a standard set of defaults ranges are
                reserved which are largely innapropriate for use in a test
                network.
        '''
        self._cache = IntCache()
        super().__init__()
        if reserve_defaults:
            self.reserve('::/128')  # reserved-unspecified
            self.reserve('::1/128')  # reserved-loopback
            self.reserve('::0000:0:0/96')  # ipv4-compatible
            self.reserve('::FFFF:0:0/96')  # ipv4-mapped
            self.reserve('FF01::/128')  # reserved-multicast
            self.reserve('FF02::/128')  # reserved-multicast
            self.reserve('FF03::/128')  # reserved-multicast
            self.reserve('FF04::/128')  # reserved-multicast
            self.reserve('FF05::/128')  # reserved-multicast
            self.reserve('FF06::/128')  # reserved-multicast
            self.reserve('FF07::/128')  # reserved-multicast
            self.reserve('FF08::/128')  # reserved-multicast
            self.reserve('FF09::/128')  # reserved-multicast
            self.reserve('FF0A::/128')  # reserved-multicast
            self.reserve('FF0B::/128')  # reserved-multicast
            self.reserve('FF0C::/128')  # reserved-multicast
            self.reserve('FF0D::/128')  # reserved-multicast
            self.reserve('FF0E::/128')  # reserved-multicast
            self.reserve('FF0F::/128')  # reserved-multicast
            self.reserve('FF01::1/128')  # all-nodes
            self.reserve('FF02::1/128')  # all-nodes
            self.reserve('FF01::2/128')  # all-routers
            self.reserve('FF02::2/128')  # all-routers
            self.reserve('FF05::2/128')  # all-routers
            self.reserve('FF02:0:0:0:0:1:FF00::/104')  # solicited-node

    def reserve(self, ipv6=None, count=None,
                # TODO IPv6Interface does not support /netmask, only /prefixlen
                # netmask=None,
                prefixlen=None, type=None, range_count=1):
        '''Reserve an unused IPv6Interface range.

        Args:
            ipv6: A specific address or network to reserve (accepts
                overlaps/collisions.)
            count: Number of addresses to reserve.
            prefixlen: Prefix length to reserve (implicit count).
            type: Type/class of address: 'unicast', 'local', 'link-local',
                'site-local', 'multicast'
            range_count: For future use.

        Return:
            IPv6InterfaceRange

        Examples:

            >>> r = IPv6InterfaceCache()
            >>> r.reserve(count=2)
            >>> r.reserve(prefixlen=80)
            >>> r.reserve('1000:2000::3:4')
            >>> r.reserve('1000:2000::/80')
            >>> r.reserve(type='unicast')

            >>> for link in core_links:
            ...     ipv6_range = testbed.ipv6_cache.reserve(prefixlen=112)
            ...     ipv6_it = iter(ipv6_range)
            ...     for interface in link.interfaces:
            ...         interface.ipv6 = next(ipv6_it)

        '''
        # http://tools.ietf.org/html/rfc2373#section-2.1
        netmask = None
        # >>> r.reserve(netmask='ffff::')

        type_ = type
        type = builtins.type
        assert range_count
        assigned = False
        # netmask -> prefixlen
        if netmask is not None:
            assert prefixlen is None
            prefixlen = IPv6Network(
                '::/{}'.format(IPv6Address(netmask))).prefixlen
        # type_ -> ipv6/prefixlen
        if type_ is not None:
            assert ipv6 is None
            if type_ == 'unicast':
                ipv6 = IPv6Address(0x20000000000000000000000000000000)
                if prefixlen is None:
                    prefixlen = 64
            elif type_ == 'local':
                ipv6 = IPv6Address(0xFC000000000000000000000000000000)
                if prefixlen is None:
                    prefixlen = 32
            elif type_ == 'link-local':
                ipv6 = IPv6Address(0xFE800000000000000000000000000000)
                if prefixlen is None:
                    prefixlen = 10
            elif type_ == 'site-local':
                ipv6 = IPv6Address(0xFEC00000000000000000000000000000)
                if prefixlen is None:
                    prefixlen = 10
            elif type_ == 'multicast':
                ipv6 = IPv6Address(0xFF100000000000000000000000000000)
                if prefixlen is None:
                    prefixlen = 128
            else:
                raise ValueError(type_)
        # ipv6 -> ipv6/prefixlen
        elif ipv6 is not None:
            assert type_ is None
            assert range_count == 1
            assigned = True
            try:
                ipv6 = IPv6Address(ipv6)
            except ValueError:
                ipv6 = IPv6Interface(ipv6)
            if type(ipv6) is IPv6Address:
                if prefixlen is None:
                    prefixlen = 128
            elif type(ipv6) is IPv6Interface:
                assert netmask is None
                assert prefixlen is None
                prefixlen = ipv6.network.prefixlen
                ipv6 = ipv6.ip

        # count|prefixlen -> bits_req, prefixlen, [tot_]ip_count, n_ip_mask
        if count is not None:
            assert not assigned
            # +2: Account for ::0 and ::ffff
            count = int(count)
            assert 1 <= count < (0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF-2)
            # NOT (count + 2 - 1).bit_length()
            bits_req = math.ceil(math.log2(count + 2))
            prefixlen = 128 - bits_req
        elif prefixlen is not None:
            assert 1 <= prefixlen <= 128
            bits_req = 128 - prefixlen
        ip_count = 1 << bits_req
        tot_ip_count = ip_count * range_count
        n_ip_mask = (0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF << bits_req) \
            & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        inv_n_ip_mask = n_ip_mask ^ 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

        if assigned:
            # A specific range is requested.
            # Go through the reserved list to see where it fits and merge or
            # add, as needed.
            n_ip_from = int(ipv6) & n_ip_mask
            res = range(n_ip_from, n_ip_from + tot_ip_count)
            self._cache.add(res)

        else:
            # An unused range is requested.
            # Find a hole in the reserved list and fill it.
            if ipv6 is not None:
                min_n_ip_from = int(ipv6)
            else:
                min_n_ip_from = 0x20000000000000000000000000000000  # unicast

            n_ip_from = min_n_ip_from
            res = self._cache.reserve(start=min_n_ip_from, count=tot_ip_count,
                                      alignment_mask=inv_n_ip_mask)
            n_ip_from = res.start

        # No post-transformation

        if bits_req > 1:
            n_ip_from = n_ip_from + 1  # .1
            if count is not None:
                ip_count = count
            else:
                ip_count = ip_count - 2  # full range except .0 and .255

        if assigned:
            start = IPv6Interface('{}/{}'.format(ipv6, prefixlen))
        else:
            start = IPv6Interface('{}/{}'.format(IPv6Address(n_ip_from),
                                                 prefixlen))

        return IPv6InterfaceRange(start, int(start.ip) + ip_count)


class MACCache(object):
    '''Generic MAC cache.

    Helper class to manage a cache of "reserved" MAC objects.

    See also:
        testbed.mac_cache
    '''

    _cache = None  # IntCache

    def __init__(self, reserve_defaults=True):
        '''Initialize the MACCache.

        Args:
            reserve_defaults: If True, a standard set of defaults ranges are
                reserved which are largely innapropriate for use in a test
                network.
        '''
        self._cache = IntCache()
        super().__init__()

        if reserve_defaults:
            self.reserve('0000.0000.0000', prefixlen=16)  # reserved
            self.reserve('FFFF.FFFF.FFFF')  # reserved-broadcast

    def reserve(self, mac=None, count=None, prefixlen=None, type=None,
                range_count=1):
        '''Reserve an unused MAC range.

        Args:
            mac: A specific address to reserve (accepts collisions.)
            count: Number of addresses to reserve.
            prefixlen: Prefix length to reserve (implicit count).
            type: Type of address: 'global', 'unicast', 'global-unicast',
                'global-multicast', 'multicast', 'local', 'local-unicast',
                'local-multicast'
            range_count: For future use.

        Return:
            MACRange

        Examples:

            >>> r = MACCache()
            >>> r.reserve(count=2)
            >>> r.reserve(prefixlen=16)
            >>> r.reserve('aaaa.bbbb.cccc')
            >>> r.reserve(type='global-multicast')

            >>> for interface in my_eth_interfaces:
            ...     interface.mac_address = \
            ...         testbed.mac_cache.reserve(count=1)[0]

        '''

        type_ = type
        type = builtins.type
        assert range_count
        assigned = False
        mac_multicast = False
        mac_local = False
        # type_ -> mac/prefixlen
        if type_ is not None:
            assert mac is None
            if (type_ == 'global'
                    or type_ == 'unicast'
                    or type_ == 'global-unicast'):
                mac_local = False
                mac_multicast = False
                if prefixlen is None:
                    prefixlen = 48
            elif type_ == 'global-multicast' or type_ == 'multicast':
                mac_local = False
                mac_multicast = True
                if prefixlen is None:
                    prefixlen = 48
            elif type_ == 'local' or type_ == 'local-unicast':
                mac_local = True
                mac_multicast = False
                if prefixlen is None:
                    prefixlen = 48
            elif type_ == 'local-multicast':
                mac_local = True
                mac_multicast = True
                if prefixlen is None:
                    prefixlen = 48
            else:
                raise ValueError(type_)
        # mac -> mac/prefixlen
        elif mac is not None:
            assert type_ is None
            assert range_count == 1
            assigned = True
            mac = MAC(mac)
            assert mac.version == 48  # TODO
            if prefixlen is None:
                prefixlen = 48

        # count|prefixlen -> bits_req, prefixlen, [tot_]ip_count, n_ip_mask
        if count is not None:
            assert not assigned
            # +0: Do NOT account for any special addresses
            count = int(count)
            assert 1 <= count < (0xFFFFFFFFFFFF-0)
            # NOT (count + 0 - 1).bit_length()
            bits_req = math.ceil(math.log2(count + 0))
            prefixlen = 48 - bits_req
        elif prefixlen is not None:
            assert 1 <= prefixlen <= 48
            bits_req = 48 - prefixlen
        ip_count = 1 << bits_req
        tot_ip_count = ip_count * range_count
        n_ip_mask = (0xFFFFFFFFFFFF << bits_req) & 0xFFFFFFFFFFFF
        inv_n_ip_mask = n_ip_mask ^ 0xFFFFFFFFFFFF

        if assigned:
            # A specific range is requested.
            # Go through the reserved list to see where it fits and merge or
            # add, as needed.
            n_ip_from = int(mac) & n_ip_mask
            # Move bits 6-7 (local/multicast) to the front
            n_ip_from = (
                (n_ip_from & 0x030000000000) << 6 |
                (n_ip_from & 0xFC0000000000) >> 2 |
                (n_ip_from & 0x00FFFFFFFFFF))
            res = range(n_ip_from, n_ip_from + tot_ip_count)
            self._cache.add(res)

        else:
            # An unused range is requested.
            # Find a hole in the reserved list and fill it.
            if mac is not None:
                min_n_ip_from = int(mac)
            else:
                # unassigned and easy to recognize
                min_n_ip_from = 0xFC0000000000
                if mac_multicast:
                    min_n_ip_from = min_n_ip_from | 0x010000000000
                if mac_local:
                    min_n_ip_from = min_n_ip_from | 0x020000000000
            # Move bits 6-7 (local/multicast) to the front
            min_n_ip_from = (
                (min_n_ip_from & 0x030000000000) << 6 |
                (min_n_ip_from & 0xFC0000000000) >> 2 |
                (min_n_ip_from & 0x00FFFFFFFFFF))
            res = self._cache.reserve(start=min_n_ip_from, count=tot_ip_count,
                                      alignment_mask=inv_n_ip_mask)
            n_ip_from = res.start

        # Move bits 6-7 (local/multicast) back to where they belong
        n_ip_from = (
            (n_ip_from & 0xC00000000000) >> 6 |
            (n_ip_from & 0x3F0000000000) << 2 |
            (n_ip_from & 0x00FFFFFFFFFF))

        # No special addresses

        if count is not None:
            ip_count = count

        if assigned:
            start = mac
        else:
            start = MAC(n_ip_from)

        return MACRange(start, int(start) + ip_count)

class QDict(dict):

    @property
    def q(self):
        if not hasattr(self, '_q_cache'):
            self._q_cache = Dq(self)
        return self._q_cache

# vim: ft=python et sw=4
