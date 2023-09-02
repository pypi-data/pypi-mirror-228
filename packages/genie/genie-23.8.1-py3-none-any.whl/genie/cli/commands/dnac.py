import os
import json
import logging
from tqdm import tqdm
from itertools import product
from collections import OrderedDict
from pyats.aetest.utils import format_filter_exception
from genie.metaparser.util.exceptions import SchemaEmptyParserError

from pyats.cli.base import Command

import urllib3

# disable HTTPS warning for clarity
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# import pcall
import importlib
try:
    pcall = importlib.import_module('pyats.async').pcall
except ImportError:
    from pyats.async_ import pcall
# # import pcall
# from pyats.async import pcall

from genie.conf import Genie
from genie.utils.summary import Summary

# internal logger
log = logging.getLogger(__name__)

FEATURES = {\
'interface':'/dna/intent/api/v1/interface',
'ospf':'/dna/intent/api/v1/interface/ospf',
'isis':'/dna/intent/api/v1/interface/isis'}


class DnacCommand(Command):
    '''
    Command to learn DNAC features and save to file (Prototype)
    '''

    name = 'dnac'
    help = 'Command to learn DNAC features and save to file (Prototype)'
    description = '''
Command to learn DNAC features and save to fil (Prototype)

    Available features: Interface, isis, ospf'''

    usage = '''{prog} [commands] [options]

Example
-------
  {prog} interface --testbed-file tb.yaml --output snapshot1
'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parser.add_argument('feature',
                                 type=str,
                                 nargs='*',
                                 help='List of Feature to learn, comma '
                                      'separated, interface, isis; all can instead '
                                      'be provided to learn all features')
        self.parser.add_argument('--testbed-file',
                                 help='specify testbed_file yaml',
                                 type=str)
        self.parser.add_argument('--devices',
                                 nargs='*',
                                 help='List of devices, comma '
                                      'separated, if not provided '
                                      'it will learn on '
                                      'all devices (Optional)')
        self.parser.add_argument('--output', default='.',
                                 help='Which directory to store logs, by '
                                      'default it will be current directory (Optional)')
        self.parser.add_argument('--single-process',
                                 action='store_true',
                                 help='Learn one device at the time instead of in parallel (Optional)')
        self.parser.add_argument('--via',
                                 nargs='*',
                                 help='List of connection to use per device "nxos-1:ssh"')

    def parse_args(self, argv):
        # inject general group options
        self.add_general_opts(self.parser)

        # do the parsing
        args, unknown = self.parser.parse_known_args(argv)
        import sys
        sys.argv = sys.argv[:1]+unknown
        return args

    def run(self, args):

        if not args.testbed_file:
            raise Exception('No --testbed-file provided, genie dnac --help '
                            'for usage')

        if not args.feature:
            raise Exception('No feature provided, genie dnac --help for usage')

        testbed = Genie.init(args.testbed_file)
        devices = args.devices if args.devices else testbed.devices

        via_args = args.via if args.via else []
        # Convert to dict
        self.vias = {}
        for device_via in via_args:
            device, via = device_via.split(':')
            self.vias[device] = via

        directory = args.output
        os.makedirs(directory, exist_ok=True)
        single = args.single_process

        self._learn_feature(args.feature, devices, directory, testbed, single)

    def _learn_feature(self, feature_list, devices, directory, testbed, single):
        '''Learn Opses features on multiple devices'''
        if len(feature_list) == 1 and feature_list[0] == 'all':
            feature_list = []
            feature_list.extend(FEATURES.keys())

        log.info("\nLearning '{o}' on devices "\
                 "'{d}'".format(o=feature_list, d=list(devices)))

        summary_table = OrderedDict()
        devices_obj = []
        for device in devices:
            if device in testbed.devices:
                dev = testbed.devices[device]
                kwargs = {}
                if dev.name in self.vias:
                    kwargs['via'] = self.vias[dev.name]
                    kwargs['alias'] = self.vias[dev.name]
                elif dev.alias in self.vias:
                    kwargs['via'] = self.vias[dev.alias]
                    kwargs['alias'] = self.vias[dev.alias]

                # set default behavior to via/alias rest
                kwargs.setdefault('via', 'rest')
                kwargs.setdefault('alias', 'rest')

                dev.connect(**kwargs)
                devices_obj.append(dev)
                summary_table[dev.name] = OrderedDict({'connected': True})
            else:
                # Decision to take - Right now its a very friendly tool.
                # Should it crash? I think staying friendly is the right way to
                # do it
                summary_table[dev.name] = OrderedDict({'connected': False})

        # If no devices exists
        if not devices_obj:
            log.error('No devices provided exists')
            return

        for feature in tqdm(feature_list):
            if single:
                output = []
                for device in devices_obj:
                    output.append(self._retrieve_feature(device, 
                                                         feature, 
                                                         directory))
            else:
                output = pcall(self._retrieve_feature, 
                               iargs = product(devices_obj,
                                               [feature],
                                               [directory]))


            for item in output:
                ops_file, console_file, exception_file, device = item

                summary_table[device][feature] = OrderedDict()
                summary_table[device][feature]['console'] = console_file
                summary_table[device][feature]['feature'] = ops_file
                summary_table[device][feature]['exception'] = exception_file

        for device, data in summary_table.items():
            # Report nicely
            summary = Summary('Genie DNAC Summary for device {d}'
                              .format(d=device), 80)

            if data['connected']:
                summary.add_message(' Connected to {d}'.format(d=device))
            else:
                summary.add_message(" Device '{d}' does not exists in the "
                                    " Testbed file".format(d=device))
            summary.add_sep_line()

            for i, items in enumerate(data.items()):
                feature, info = items
                if feature == 'connected':
                    continue

                if info['exception']:
                    # Could not learn this feature
                    summary.add_message(" Could not learn '{o}'".format(o=feature))
                    if info['exception']:
                        summary.add_message(' -  Exception:      {l}'
                                            .format(l=info['exception']))
                    if info['feature'] is None and info['console'] is None:
                        dev = testbed.devices[device]
                        if dev.os == 'generic':
                            summary.add_message(" -  Mandatory field 'os' was "
                                                "not given in the yaml file")
                        else:
                            summary.add_message(" -  Feature not yet developed for this os")
                        if not i == len(data)-1:
                            summary.add_sep_line()
                        continue
                else:
                    summary.add_message(" Learnt '{o}'".format(o=feature))

                summary.add_message(' -  output:  {l}'
                                    .format(l=info['feature']))
                if not i == len(data)-1:
                    summary.add_sep_line()
            summary.add_subtitle_line()
            summary.print()
            log.info('\n')


    def _retrieve_feature(self, device, feature, directory):

        # Save to file the structure
        fname = feature.replace('/','-').lstrip('-')
        feature_file_name = "{dir}/{o}_{do}_{dn}_feature.txt"\
                            .format(o=fname,
                                    do=device.os,
                                    dn=device.name,
                                    dir=directory)

        exception_file_name = None

        via = self.vias.get(device.name, self.vias.get(device.alias, 'rest'))

        if feature in FEATURES:
            try:
                output = device.parse(FEATURES[feature], alias=via)
            except SchemaEmptyParserError:
                # Empty but that's okay
                output = {}
            except Exception as e:
                exception_file_name = "{dir}/{o}_{do}_{dn}_exception.txt"\
                                    .format(o=fname,
                                            do=device.os,
                                            dn=device.name,
                                            dir=directory)
                msg = 'Issue while learning the feature\n\n'
                with open(exception_file_name, 'w') as f:
                    f.write(msg)
                    f.write(format_filter_exception(exc_type=type(e),
                                                    exc_value=e,
                                                    tb=e.__traceback__))
                return (None, None, exception_file_name, device.name)
                

        else:
            # generic flow
            try:
                resp = device.connectionmgr.connections[via].get(feature)

                output = resp.json()
            except Exception as e:
                
                exception_file_name = "{dir}/{o}_{do}_{dn}_exception.txt"\
                                    .format(o=fname,
                                            do=device.os,
                                            dn=device.name,
                                            dir=directory)
                msg = 'Issue while learning the feature\n\n'
                with open(exception_file_name, 'w') as f:
                    f.write(msg)
                    f.write(format_filter_exception(exc_type=type(e),
                                                    exc_value=e,
                                                    tb=e.__traceback__))
                return (None, None, exception_file_name, device.name)

        with open(feature_file_name, 'w') as f:
            f.write(json.dumps(output, 
                               sort_keys=True, 
                               indent=2, 
                               separators=(',', ': ')))

        return (feature_file_name, None, exception_file_name, device.name)