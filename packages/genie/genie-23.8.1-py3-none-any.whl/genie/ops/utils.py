import os
import json
import pathlib
import logging
import importlib
from genie.abstract import Lookup
from pyats import configuration as cfg
from pkg_resources import iter_entry_points
from genie.metaparser.util import merge_dict
from genie.json.make_json import MakeOps as GenieMakeOps

EXCLUDE_OPS = ['__init__.py', '__pycache__', 'tests', 'vxlan_consistency']
PYATS_EXT_OPS = 'pyats.libs.external.ops'
OPS_ENTRYPOINT = 'genie.libs.ops'

log = logging.getLogger(__name__)
ops_data = None


class ExtendOps(GenieMakeOps):

    def __init__(self, package):
        self.output = {'tokens': []}
        self.package = package
        self.root = {
            'root': package,
            'mod_name': 'ops',
            'url': {
                'link': 'https://wwwin-github.cisco.com/pyATS/genielibs.cisco/tree/{branch}/',
                'branch': 'dev',
                'style': 'github',
            },
        }
        self.module_loc = importlib.import_module(package).__path__[0]
        self.package_location = self.module_loc

    def extend(self):
        """ Recursively find the ops objects in the external package
            and store the information into self.output dictionary """
        self._recursive_find(pathlib.Path(self.module_loc), [])

def _load_ops_json():
    """Discover Ops data from multiple sources.

    First load data from the ops.json file. Then extend the data by searching
    for more Ops in an optional external Ops package and in any genie.libs.ops
    entrypoint packages

    Args:
        None

    Returns:
        A dictionary of Ops data containing features as keys and associated Ops 
        class info organized by tokens as values. For example:

        {'acl': {
            'ios': {
                'class_name': 'Acl',
                'doc': None,
                'module_name': 'acl.acl',
                'package': 'genie.libs.ops',
                'uid': 'acl',
                'url': '<someURL>'},
            'iosxe': {
                'class_name': 'Acl',
                'doc': 'ACL Genie Ops Object',
                'module_name': 'acl.acl',
                'package': 'genie.libs.cisco.ops',
                'uid': 'acl',
                'url': '<someURL>'},
            ...
        'lag': {
            'nxos': {
                'class_name': 'Lag',
                'doc': None,
                'module_name': 'lag.lag',
                'package': 'some.custom.package',
                'uid': 'lag',
                'url': '<someURL>'},
        ...
        }

    Raises:
        None
    """

    try:
        mod = importlib.import_module("genie.libs.ops")
        functions = os.path.join(mod.__path__[0], "ops.json")
    except Exception:
        functions = ""

    if not os.path.isfile(functions):
        log.warning(
            "ops.json does not exist, make sure you "
            "are running with latest version of "
            "genie.libs.ops"
        )
        return {}

    # Open all the Ops in json file
    with open(functions) as f:
        function_data = json.load(f)

    # Check Ops entrypoints (like within genielibs.cisco)
    for entry in iter_entry_points(group=OPS_ENTRYPOINT):
        log.info('Loading Ops from {}'.format(entry.module_name))

        ext = ExtendOps(entry.module_name)
        ext.extend()
        ext.output.pop('tokens', None)
        log.info("{} extended Ops count: {}".format(
            entry.module_name,
            len(ext.output.keys())))
        log.debug('{} Ops {}'.format(
            entry.module_name,
            json.dumps(ext.output, indent=4)
        ))
        function_data = merge_dict(function_data, ext.output, update=True)

    # Check if provided external ops packages
    ext_ops_package = cfg.get(PYATS_EXT_OPS, None) or \
        os.environ.get(PYATS_EXT_OPS.upper().replace('.', '_'))

    if ext_ops_package:
        ext = ExtendOps(ext_ops_package)
        ext.extend()
        ext.output.pop('tokens', None)
        function_data = merge_dict(function_data, ext.output, update=True)

    return function_data

def get_ops(feature, device):
    """Return the ops class for a given feature.

    Combines the data from _load_ops_json() with Abstraction Lookup to find the
    Ops class for a given feature and device

    Args:
        feature (str): The feature to be learned
        device (obj): The device that the feature will be learned on

    Returns:
        class: The Ops class for the feature to be learned

    Raises:
        LookupError: if the Ops can't be found
    """

    global ops_data
    if ops_data is None:
        ops_data = _load_ops_json()

    # Lookup the feature in the Ops json data
    try:
        data = ops_data[feature]
    except KeyError:
        raise LookupError("Could not find a feature called '{c}'".format(
            c=feature)) from None

    # Get the device tokens and drill down into the feature's abstraction keys
    tokens = Lookup.tokens_from_device(device)
    for token in tokens:
        if token in data:
            data = data[token]

    ops_package = importlib.import_module(data['package'])
    lookup = Lookup.from_device(device, packages={"ops": ops_package})
    try:
        return getattr(
            _get_submodule(lookup.ops, data['module_name']), data['class_name']
        )
    except Exception:
        raise LookupError(
            f"Could not find an Ops feature called '{feature}' under {device.os}") from None

def _get_submodule(abs_mod, mods):
    """recursively find the submodule"""
    if "." not in mods:
        return getattr(abs_mod, mods)
    current, next = mods.split(".", 1)
    mod = getattr(abs_mod, current)
    try:
        return getattr(mod, next)
    except Exception:
        pass
    return _get_submodule(mod, next)

def get_ops_exclude(feature, device):
    try:
        return get_ops(feature, device).exclude
    except AttributeError:
        return []

def get_ops_features():
    """Gets a list with all available Ops features

    Uses the dictionary keys from _load_ops_json() to produce a list of all
    available Ops features that can be learned. Used when device.learn("all")
    is called. Also appends 'config' to the list to be returned

    Args:
        None

    Returns:
        list: List of all available Ops features

    Raises:
        None
    """
    global ops_data
    if ops_data is None:
        ops_data = _load_ops_json()

    # Figure out what to learn
    ops_list = []
    for ops in sorted(list(ops_data.keys())):
        if ops not in EXCLUDE_OPS and ops != 'tokens':
            ops_list.append(ops)
    ops_list.append("config")

    return ops_list
