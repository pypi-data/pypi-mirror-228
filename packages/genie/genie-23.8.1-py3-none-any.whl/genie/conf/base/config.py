import logging
import functools

try:
    from ydk.types import Empty
    from ydk.models.ietf import ietf_netconf
    from ydk.services import CRUDService
    from ydk.services import CodecService
    from ydk.providers import CodecServiceProvider
except Exception:
    pass

from unicon.statemachine import State

log = logging.getLogger(__name__)

@functools.total_ordering
class Config(object):
    '''Delayed configuration to be applied on a Device

    This object is a self contained configuration, which can
    be applied on a device without extra arguments.
    '''

    def __init__(self, device, unconfig=False, **kwargs):
        '''Initialize a Config instance.

        Args:
            device (`Device`): Device object
            unconfig: default is False. When True, unconfig mode is turned on
                      and unconfiguration config is given
        '''
        self.device = device
        self.unconfig = unconfig
        self.fkwargs = kwargs

    def __eq__(self, other):
        '''Implement `self == other`.

        Two Config instances are equal if they both apply to the same device,
        with the same `unconfig` mode, the same keyword arguments and have the
        same string representation.
        '''
        if not isinstance(other, Config):
            return NotImplemented
        v1 = (
            self.device,
            self.unconfig,
            self.fkwargs,
        )
        v2 = (
            other.device,
            other.unconfig,
            other.fkwargs,
        )
        # String representation could be costly; Avoid if possible.
        return v1 == v2 and str(self) == str(other)

    def __lt__(self, other):
        '''Implement `self < other`.'''
        if not isinstance(other, Config):
            return NotImplemented
        v1 = (
            self.device,
            self.unconfig,
            self.fkwargs,
        )
        v2 = (
            other.device,
            other.unconfig,
            other.fkwargs,
        )
        # String representation could be costly; Avoid if possible.
        return v1[:2] < v2[:2] \
            or (v1 == v2 and str(self) < str(other))


class CliConfig(Config):
    '''Delayed configuration to be applied on a Device

    This object is a self contained configuration, which can
    be applied on a device without extra arguments.
    '''

    def __init__(self, cli_config, **kwargs):
        '''Initialize a Config instance.

        Args:
            device (`Device`): Device object
            unconfig: (`Bool`): default is False. When True, unconfig mode is
                                turned on and unconfiguration config is given
            cli_config: (`str`): Configuration to apply on the device

        '''
        super().__init__(**kwargs)
        self.cli_config = cli_config

    def __str__(self):
        '''String representation of the configuration'''
        return str(self.cli_config)

    def apply(self, **kwargs):
        '''Apply the configuration on the device. Extra kwargs will be
        passed to the device'''
        value = str(self.cli_config)
         # Merge kwargs with fkwargs, where kwargs take priority
        _kwargs = self.fkwargs.copy()
        _kwargs.update(kwargs)
        if value:
            self.device.cli.configure(value, **_kwargs)


class YangConfig(Config):
    '''Delayed configuration to be applied on a Device via Yang

    This object is a self contained configuration, which can
    be applied on a device without extra arguments.
    '''

    def __init__(self, ydk_obj, ncp, crud_service, **kwargs):
        '''Initialize a Config instance for Yang.

        Args:
            device (`Device`): Device object
            unconfig: (`Bool`): default is False. When True, unconfig mode is
                                turned on and unconfiguration config is given
            ydk_obj (`Ydk`): Ydk object holding the attributes
            ncp: (`NetconfServiceProvider`):  NetconfServiceProvider object
            crud_service (`CRUDService`) : CRUDService object
        '''
        super().__init__(**kwargs)
        self.ydk_obj = ydk_obj
        self.ncp = ncp
        self.crud_service = crud_service

    def __str__(self):
        edit_config = ietf_netconf.EditConfigRpc()
        edit_config.input.target.running = Empty()
        edit_config.input.config = self.ydk_obj

        codec = CodecService()
        codec_p = CodecServiceProvider(type='xml')

        payload = codec.encode(codec_p, edit_config)
        return payload

    def apply(self, **kwargs):
        '''Apply Yang configuration on the device'''
        # instantiate crud service
        # create netconf connection
        ncp = self.ncp(self.device)
        self.crud_service(ncp, self.ydk_obj)

class RestConfig(Config):
    '''Delayed configuration to be applied on a Device

    This object is a self contained configuration, which can
    be applied on a device without extra arguments.
    '''

    def __init__(self, dn, cli_payload, partition, buffer_size=20000, **kwargs):
        '''Initialize a Config instance.

        Args:
            device (`Device`): Device object
            unconfig: (`Bool`): default is False. When True, unconfig mode is
                                turned on and unconfiguration config is given
            dn: (`str`): Unique distinguished name that describes the object
                         and its place in the tree
            cli_payload (`str`): cli config to send via REST to the device
            partition (`str`): Where to partition on the returned output from
                               the device
            buffer_size (`int`): desired buffer size.

        '''
        super().__init__(**kwargs)
        self.dn = dn
        self.cli_payload = cli_payload
        self._partition = partition
        self.buffer_size = buffer_size

    def __str__(self):
        '''String representation of the configuration'''
        return str(self.cli_payload)

    def apply(self, **kwargs):
        '''Apply the configuration on the device. Extra kwargs will be
        passed to the device'''

        # Now convert to REST by calling the device

        log.info('Sending Sandbox command to learn REST config')

        # Set to the configuration state
        pattern = r'^{d}(config-s)#\s?$'.format(d=self.device.name)
        State(name='config', pattern=pattern)

        try:
            ret = self.device.cli.configure(self.cli_payload)
        finally:
            # Reverse back to the original state
            State(name='config', pattern=r'^.(%N\(config\))#\s?')

        # Remove configuration from output
        ret = ret.rpartition(self._partition)[-1]
        # And remove everything after the last }
        ret = ret[:ret.rindex('}') + 1]

        # This is the rest to apply on the device
        self.device.rest.post(payload=ret, dn=self.dn)
