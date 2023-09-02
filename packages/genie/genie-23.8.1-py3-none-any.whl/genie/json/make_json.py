#
# The 'package_location' attribute is indented to be used to point to the 'root' of the repository
# and asssumes the package is installed in developer mode. This is used to create the URL for
# GitHub source references and to store references to the datafiles in the DATAFILES variable.
#
# The 'module_loc` attribute is intended to point to the 'root' of the 'library', e.g. genie.libs.clean
# and is used to find the modules below that.
#

import os
import sys

import sys
import json
import yaml
import logging
import pathlib
import inspect
import itertools
import importlib
import pkg_resources

from genie.metaparser import MetaParser
from genie.libs.sdk.genie_yamls import datafile
from genie.json.exceptions import ApiImportError
from pyats.async_ import pcall

log = logging.getLogger(__name__)

PACKAGE_LOCATIONS = {
    'parsers': [p for p in pkg_resources.working_set if p.project_name == 'genie.libs.parser'][0].location,
    'apis': [p for p in pkg_resources.working_set if p.project_name == 'genie.libs.sdk'][0].location,
    'ops': [p for p in pkg_resources.working_set if p.project_name == 'genie.libs.ops'][0].location,
    'models': [p for p in pkg_resources.working_set if p.project_name == 'genie.libs.sdk'][0].location,
    'trigger': [p for p in pkg_resources.working_set if p.project_name == 'genie.libs.sdk'][0].location,
    'verification': [p for p in pkg_resources.working_set if p.project_name == 'genie.libs.sdk'][0].location,
    'clean': [p for p in pkg_resources.working_set if p.project_name == 'genie.libs.clean'][0].location,
}

# Start path with '../<package>/' so paths can resolve from any package
DATAFILES = {
    'parsers': {
        PACKAGE_LOCATIONS['parsers'] + '/../sdk_generator/github/parser_datafile.yaml': \
            PACKAGE_LOCATIONS['parsers'] + '/../sdk_generator/outputs/github_parser.json',
    },
    'apis': {
        PACKAGE_LOCATIONS['apis'] + '/../../sdk-pkg/sdk_generator/github/api_datafile.yaml': \
            PACKAGE_LOCATIONS['apis'] + '/../../sdk-pkg/sdk_generator/output/github_apis.json',
    },
    'ops': {
        PACKAGE_LOCATIONS['ops'] + '/../../ops-pkg/ops_generator/github/ops_datafile.yaml': \
            PACKAGE_LOCATIONS['ops'] + '/../../ops-pkg/ops_generator/output/github_ops.json',
    },
    'models': {
        PACKAGE_LOCATIONS['models'] + '/../../sdk-pkg/sdk_generator/github/models.yaml': \
            PACKAGE_LOCATIONS['models'] + '/../../sdk-pkg/sdk_generator/output/github_models.json',
    },
    'triggers': {
        PACKAGE_LOCATIONS['trigger'] + '/../../sdk-pkg/sdk_generator/github/trigger_datafile.yaml': \
            PACKAGE_LOCATIONS['trigger'] + '/../../sdk-pkg/sdk_generator/output/github_triggers.json',
    },
    'verifications': {
        PACKAGE_LOCATIONS['verification'] + '/../../sdk-pkg/sdk_generator/github/verification_datafile.yaml': \
            PACKAGE_LOCATIONS['verification'] + '/../../sdk-pkg/sdk_generator/output/github_verifications.json',
    },
    'clean': {
        PACKAGE_LOCATIONS['clean'] + '/../../clean-pkg/sdk_generator/github/clean_datafile.yaml': \
            PACKAGE_LOCATIONS['clean'] + '/../../clean-pkg/sdk_generator/output/github_clean.json'
    }
}

# Check if python is running inside virtual environment and return path
def get_environment_path():
    def is_in_virtual_env():
        return (hasattr(sys, 'real_prefix') or
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))
    if is_in_virtual_env():
        return os.environ['VIRTUAL_ENV']
    return sys.prefix

class MakeParsers(object):
    # Files and directories to ignore while walking package
    IGNORE_DIR = ['.git', '__pycache__', 'template', 'tests']
    IGNORE_FILE = ['__init__.py', 'base.py', 'utils.py']

    def __init__(self, datafile):
        with open(datafile, 'r') as f:
            self.datafile = yaml.safe_load(f)

        self.output = {'tokens': []}
        self.package_location = PACKAGE_LOCATIONS['parsers']

    def _format_schema(self, d, tab=0):
        s = ['{\n']
        if d is None:
            return d
        for k, v in d.items():
            if isinstance(v, dict):
                v = self._format_schema(v, tab + 1)
            else:
                v = repr(v)
            s.append('%s%r: %s,\n' % ('  ' * tab, k, v))
        s.append('%s}' % ('  ' * tab))
        return ''.join(s)

    @staticmethod
    def _find_parsers(mod):
        parsers = []
        for name, obj in inspect.getmembers(mod):
            # skip if starts with '_' or not class
            if name.startswith('_') or not inspect.isclass(obj):
                continue

            # skip anything not defined in this module
            try:
                if inspect.getsourcefile(obj) != mod.__file__:
                    continue
            except:
                # getsourcefile fails for builtin objects
                # we aren't interested in those anyway
                continue

            # Inherits from MetaParser + has an attribute called 'cli_command'
            if issubclass(obj, MetaParser) and hasattr(obj, 'cli_command'):
                parsers.append(obj)

        return parsers

    def _add_parser(self, parser, cli, tokens, mod):
        if cli not in self.output:
            self.output[cli] = {}

        output = self.output[cli]
        for token in tokens:
            if token not in output:
                output[token] = {}
            output = output[token]
            if token not in self.output['tokens']:
                self.output['tokens'].append(token)

        self.output['tokens'] = sorted(self.output['tokens'])

        output['module_name'] = mod.__name__.rsplit('.', 1)[-1]
        output['package'] = self.package
        output['class'] = parser.__name__
        output['doc'] = parser.__doc__
        output['schema'] = self._format_schema(parser.schema)
        output['uid'] = cli.replace(' ', '_').replace('{', '').replace('}', '').replace('|', '_')
        line = inspect.getsourcelines(parser)[-1]

        temp_url = mod.__file__.replace(self.package_location + '/', '')

        style = self.root['url']['style']

        if style == 'bitbucket':
            url = '{p}{t}#{l}'.format(p=self.root['url']['link'], t=temp_url, l=line)
        elif style == 'github':
            url = self.root['url']['link'].format(branch=self.root['url']['branch'])
            url = '{p}src/{t}#L{l}'.format(p=url, t=temp_url, l=line)

        output['url'] = url

    def _add_parsers(self, item, tokens):
        # Find all classes which has a function named parse
        # Will give module path
        module_path = self.root['root'] + str(item).rsplit('.', 1)[0].\
            replace(self.module_loc, '').replace('/', '.')

        try:
            mod = importlib.import_module(module_path)
        except Exception as err:
            raise Exception("Cannot import parser in {module} with error: "
                            "{err}".format(module=module_path, err=str(err)))

        parsers = self._find_parsers(mod)

        for parser in parsers:
            if isinstance(parser.cli_command, list):
                for cli in parser.cli_command:
                    self._add_parser(parser, cli, tokens, mod)
            else:
                self._add_parser(parser, parser.cli_command, tokens, mod)

    def _recursive_find(self, item, token):
        for item in item.iterdir():
            if item.is_dir():
                # ignore directories in IGNORE_DIR or starting with dot, e.g. '.vscode'
                if item.name in self.IGNORE_DIR or item.name[0] == '.':
                    continue

                self._recursive_find(item, token + [item.name])

            elif item.is_file():
                if item.name in self.IGNORE_FILE or item.suffix != '.py':
                    continue

                # item is not a directory. item is not a file in IGNORE_FILE.
                # item is a python file. Find all parsers in file.
                self._add_parsers(item, token)

    def make(self):
        if 'root_directories' not in self.datafile:
            return {}

        for name, values in self.datafile['root_directories'].items():
            log.info("Learning '{name}'".format(name=name))

            # Figure out location of package so you can walk it
            self.root = values
            self.package = self.root['root']
            self.module_loc = importlib.import_module(self.root['root']).__path__[0]

            # Walk all file in there and go through the parsers
            self._recursive_find(pathlib.Path(self.module_loc), [])


class MakeApis(object):
    IGNORE_DIR = ['.git', '__pycache__', 'tests']
    IGNORE_FILE = ['__init__.py', 'base.py', 'common.py']

    def __init__(self, datafile):
        with open(datafile, 'r') as f:
            self.datafile = yaml.safe_load(f)
        self.output = {'tokens': []}
        self.package_location = PACKAGE_LOCATIONS['apis']
        if self.package_location[-3:] == 'src':
            self.package_location = '/'.join(self.package_location.split('/')[:-3])

    def _expand(self, name):
        if '$env(VIRTUAL_ENV)' in name:
            # Replace '$env(VIRTUAL_ENV)' with the actual value
            return name.replace('$env(VIRTUAL_ENV)', get_environment_path())
        return name

    # get all functions in a module
    def _find_functions(self, mod, tokens):
        abs_mod_name = self._get_mod_name(mod)
        for name, obj in sorted(inspect.getmembers(mod)):
            # starts with _ are ignored
            if name.startswith('_'):
                continue
            # ignore the imported functions
            if inspect.isfunction(obj) and obj.__module__ == mod.__name__:
                sub_dict = self.output.setdefault(name, {})
                if not tokens:
                    tokens = ['com']
                for token in tokens:
                    if token not in sub_dict:
                        sub_dict[token] = {}
                    if token not in self.output['tokens']:
                        self.output['tokens'].append(token)
                    sub_dict = sub_dict[token]

                self.output['tokens'] = sorted(self.output['tokens'])

                sub_dict['module_name'] = abs_mod_name
                sub_dict['package'] = self.package
                sub_dict['doc'] = obj.__doc__
                sub_dict['uid'] = name
                line = inspect.getsourcelines(obj)[-1]

                temp_url = mod.__file__.replace(self.package_location + '/', '')

                style = self.root['url']['style']

                if style == 'bitbucket':
                    url = '{p}{t}#{l}'.format(p=self.root['url']['link'], t=temp_url, l=line)
                elif style == 'github':
                    url = self.root['url']['link'].format(branch=self.root['url']['branch'])
                    url = '{p}{t}#L{l}'.format(p=url, t=temp_url, l=line)

                sub_dict['url'] = url

                if 'extend_info' in self.output:
                    extend_info = self.output['extend_info']
                    extend_info.append("api name: '{}', tokens {}, module name: {}"
                                .format(name, tokens, abs_mod_name))

    def _get_mod_name(self, mod):
        mod_name = []
        name_list = mod.__name__.replace(self.root['root'], '').split('.')
        # if directory is abstracted
        for i, e in enumerate(name_list):
            if not hasattr(importlib.import_module(self.root['root'] + '.'.join(name_list[0:i+1])), '__abstract_token'):
                mod_name.append(e)
        return '.'.join(mod_name)[1:]

    def _is_abstract_dir(self, dir):
        mod = str(dir).replace(self.module_loc, '').replace('/', '.')
        return hasattr(importlib.import_module(mod, package=self.root['root']), '__abstract_token')

    def _add_functions(self, item, tokens):
        # Will give module path
        module_path = self.root['root'] + str(item).rsplit('.', 1)[0].\
                                  replace(self.module_loc, '').replace('/', '.')

        # Try to import APIs, raise custom exception if a module error is found
        try:
            mod = importlib.import_module(module_path)
        except Exception:
            raise ApiImportError

        self._find_functions(mod, tokens)

    def _recursive_find(self, item, token):
        for item in item.iterdir():
            if item.is_dir():
                # ignore directories in IGNORE_DIR or starting with dot, e.g. '.vscode'
                if item.name in self.IGNORE_DIR or item.name[0] == '.':
                    # Ignore
                    continue
                elif self._is_abstract_dir(item.as_posix()):
                    self._recursive_find(item, token + [item.name])
                else:
                    self._recursive_find(item, token)

            elif item.is_file():
                if item.name in self.IGNORE_FILE or item.suffix != '.py':
                    continue
                # Then add it to the self.datafile
                self._add_functions(item, token)

    def make(self):
        if 'root_directories' not in self.datafile:
            return {}

        for name, values in self.datafile['root_directories'].items():
            log.info("Learning '{name}'".format(name=name))

            # Figure out location of package so you can walk it
            self.root = values
            self.package = self.root['root']
            self.module_loc = importlib.import_module(self.root['root']).__path__[0]

            # Walk all file in there and go through the apis
            self._recursive_find(pathlib.Path(self.module_loc), [])


class MakeClean(MakeApis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.package_location = PACKAGE_LOCATIONS['clean']
        if self.package_location[-3:] == 'src':
            self.package_location = '/'.join(self.package_location.split('/')[:-3])

    # get all functions in a module
    def _find_functions(self, mod, tokens):
        abs_mod_name = self._get_mod_name(mod)
        for name, obj in inspect.getmembers(mod):
            # starts with _ are ignored
            if name.startswith('_'):
                continue
            if abs_mod_name != 'stages.stages':
                continue
            # ignore the imported functions
            if inspect.isclass(obj) and obj.__module__ == mod.__name__:
                sub_dict = self.output.setdefault(name, {})
                if not tokens:
                    tokens = ['com']
                for token in tokens:
                    if token not in sub_dict:
                        sub_dict[token] = {}
                    if token not in self.output['tokens']:
                        self.output['tokens'].append(token)
                    sub_dict = sub_dict[token]

                self.output['tokens'] = sorted(self.output['tokens'])

                sub_dict['package'] = self.package
                sub_dict['module_name'] = abs_mod_name
                sub_dict['doc'] = obj.__doc__
                sub_dict['uid'] = name
                line = inspect.getsourcelines(obj)[-1]

                temp_url = mod.__file__.replace(self.package_location + '/', '')

                style = self.root['url']['style']

                if style == 'bitbucket':
                    url = '{p}{t}#{l}'.format(p=self.root['url']['link'], t=temp_url, l=line)
                elif style == 'github':
                    url = self.root['url']['link'].format(branch=self.root['url']['branch'])
                    url = '{p}{t}#L{l}'.format(p=url, t=temp_url, l=line)

                sub_dict['url'] = url


class MakeOps(object):
    IGNORE_DIR = ['.git', '__pycache__', 'template', 'tests', 'utils']
    IGNORE_FILE = ['__init__.py', 'base.py', 'common.py']

    def __init__(self, datafile):
        with open(datafile, 'r') as f:
            self.datafile = yaml.safe_load(f)

        self.output = {'tokens': []}
        self.package_location = PACKAGE_LOCATIONS['ops']
        if self.package_location[-3:] == 'src':
            self.package_location = '/'.join(self.package_location.split('/')[:-3])
        self.package = "genie.libs.ops"

    def _expand(self, name):
        if '$env(VIRTUAL_ENV)' in name:
            # Replace '$env(VIRTUAL_ENV)' with the actual value
            return name.replace('$env(VIRTUAL_ENV)', get_environment_path())
        return name

    def _find_ops(self, mod, tokens):
        for name, obj in inspect.getmembers(mod):
            # starts with _ are ignored
            if name.startswith('_'):
                continue
            # ignore the imported functions
            if inspect.isclass(obj) and obj.__module__ == mod.__name__:
                sub_dict = self.output.setdefault(mod.__name__.split('.')[-1], {})
                for token in tokens:
                    if token not in sub_dict:
                        sub_dict[token] = {}
                    if token not in self.output['tokens']:
                        self.output['tokens'].append(token)

                    sub_dict = sub_dict[token]
                    sub_dict['module_name'] = self._get_mod_name(mod)
                    sub_dict['doc'] = obj.__doc__
                    sub_dict['uid'] = name.lower()
                    sub_dict['class_name'] = name
                    sub_dict['package'] = self.package
                    line = inspect.getsourcelines(obj)[-1]
                    temp_url = mod.__file__.replace(self.package_location + '/', '')
                    style = self.root['url']['style']
                    if style == 'bitbucket':
                        url = '{p}{t}#{l}'.format(p=self.root['url']['link'], t=temp_url,
                                                  l=line)
                    elif style == 'github':
                        url = self.root['url']['link'].format(
                            branch=self.root['url']['branch'])
                        url = '{p}{t}#L{l}'.format(p=url, t=temp_url, l=line)
                    # update only when token is deepest so that preventing
                    # base token such as 'iosxe', 'nxos' is overwritten
                    if 'url' not in sub_dict or token == tokens[-1]:
                        sub_dict['url'] = url
                self.output['tokens'] = sorted(self.output['tokens'])

    def _get_mod_name(self, mod):
        mod_name = []
        name_list = mod.__name__.replace(self.root['root'], '').split('.')
        # if directory is abstracted
        for i, e in enumerate(name_list):
            if not hasattr(importlib.import_module(self.root['root'] + '.'.join(name_list[0:i+1])), '__abstract_token'):
                mod_name.append(e)
        return '.'.join(mod_name)[1:]

    def _add_ops(self, item, tokens):
        module_path = self.root['root'] + str(item).rsplit('.', 1)[0]. \
            replace(self.module_loc, '').replace('/', '.')
        mod = importlib.import_module(module_path)
        self._find_ops(mod, tokens)

    def _is_abstract_dir(self, dir):
        mod = str(dir).replace(self.module_loc, '').replace('/', '.')
        return hasattr(importlib.import_module(mod, package=self.root['root']), '__abstract_token')

    def _recursive_find(self, item, token):
        for item in item.iterdir():
            if item.is_dir():
                # ignore directories in IGNORE_DIR or starting with dot, e.g. '.vscode'
                if item.name in self.IGNORE_DIR or item.name[0] == '.':
                    # Ignore
                    continue
                elif self._is_abstract_dir(item.as_posix()):
                    self._recursive_find(item, token + [item.name])
                else:
                    self._recursive_find(item, token)
            elif item.is_file():
                if item.name in self.IGNORE_FILE or item.suffix != '.py':
                    continue
                # Then add it to the self.datafile
                self._add_ops(item, token)

    def make(self):
        if 'root_directories' not in self.datafile:
            return {}

        for name, values in self.datafile['root_directories'].items():
            log.info("Learning '{name}'".format(name=name))

            # Figure out location of package so you can walk it
            self.root = values
            self.module_loc = importlib.import_module(self.root['root']).__path__[0]

            # Walk all file in there and go through the apis
            self._recursive_find(pathlib.Path(self.module_loc), [])


class MakeModels(object):
    AVAILABLE_OPS_CONF_FEATURES = [
        'acl', 'arp', 'bgp', 'dot1x', 'eigrp', 'fdb', 'hsrp',
        'igmp', 'interface', 'isis', 'lisp', 'lldp', 'mcast', 'mld',
        'msdp', 'nd', 'ntp', 'ospf', 'pim', 'prefix_list', 'rip',
        'route_policy', 'routing', 'static_routing', 'stp',
        'vlan', 'vrf', 'vxlan'
    ]

    MODELS_ONLY = []

    # if conf is ready and ops is not ready
    # fill just_conf_ready
    ONLY_CONF = [
        'l2vpn', 'segment_routing'
    ]

    # if ops is ready and conf is not ready
    ONLY_OPS = [
        'lag', 'platform'
    ]

    def __init__(self, datafile):
        self.output = {}

        # Parse the datafile
        with open(datafile, 'r') as f:
            self.datafile = yaml.safe_load(f)
        self.conf_repo = self.datafile['repo_path_conf']
        self.ops_repo = self.datafile['repo_path_ops']
        self.branch = self.datafile['branch']
        self.style = self.datafile['style']

    def make(self):
        log.info("Learning 'Models'")

        if self.style == 'bitbucket':
            conf_path = '{path}/conf/{feature}{branch}'
            ops_path = '{path}/ops/{feature}{branch}'
        elif self.style == 'github':
            self.conf_repo = self.conf_repo.format(branch=self.branch)
            self.ops_repo = self.ops_repo.format(branch=self.branch)
            conf_path = '{path}/conf/{feature}'
            ops_path = '{path}/ops/{feature}'

        for feature in self.AVAILABLE_OPS_CONF_FEATURES:
            temp = {'file': '_models/{feature}.pdf'.format(feature=feature),
                    'conf': conf_path.format(path=self.conf_repo, feature=feature, branch=self.branch),
                    'ops': ops_path.format(path=self.ops_repo, feature=feature, branch=self.branch)}

            self.output[feature] = temp

        for feature in self.MODELS_ONLY:
            temp = {'file': '_models/{feature}.pdf'.format(feature=feature),
                    'conf': '',
                    'ops': ''}
            self.output[feature] = temp

        for feature in self.ONLY_CONF:
            temp = {'file': '_models/{feature}.pdf'.format(feature=feature),
                    'conf': conf_path.format(path=self.conf_repo, feature=feature, branch=self.branch),
                    'ops': ''}

            self.output[feature] = temp

        for feature in self.ONLY_OPS:
            temp = {'file': '_models/{feature}.pdf'.format(feature=feature),
                    'conf': '',
                    'ops': ops_path.format(path=self.ops_repo, feature=feature, branch=self.branch)}
            self.output[feature] = temp


class MakeTriggersVerifications(object):
    CONTEXTS = ['cli', 'yang', 'xml', 'rest']
    IGNORE_DIR = ['.git', '__pycache__', 'tests']
    IGNORE_FILE = ['__init__.py']

    def __init__(self, datafile, type_):
        self.output = {
            'tokens': [],
            'testcases': []
        }

        # Parse the datafile
        with open(datafile, 'r') as f:
            self.datafile = yaml.safe_load(f)

        self.type_ = type_
        self.mode = 'trigger' if self.type_ == 'triggers' else 'verification'
        if self.mode == 'trigger':
            self.package_location = PACKAGE_LOCATIONS['apis']
            if self.package_location[-3:] == 'src':
                self.package_location = '/'.join(self.package_location.split('/')[:-2])
        else:
            self.package_location = PACKAGE_LOCATIONS['parsers']
            if self.package_location[-3:] == 'src':
                self.package_location = '/'.join(self.package_location.split('/')[:-1])

    @staticmethod
    def _find_diff(l1, l2):
        '''Difference between list1 and list2'''
        diff = []
        for list1, list2 in itertools.zip_longest(l1, l2):
            if list2 != list1:
                diff.append(list2)
        return diff

    def _expand(self, name):
        if '$env(VIRTUAL_ENV)' in name:
            # Replace '$env(VIRTUAL_ENV)' with the actual value
            return name.replace('$env(VIRTUAL_ENV)', get_environment_path())
        return name

    def make(self):

        if 'root_directories' not in self.datafile:
            return {}

        for name, values in self.datafile['root_directories'].items():
            log.info("Learning '{name}'".format(name=name))
            if 'yaml' not in values:
                continue

            # Find trigger datafile for trigger/verification for Callable

            yaml_file = datafile(self.mode, values['yaml'])

            with open(yaml_file, 'r') as f:
                content = yaml.safe_load(f)
            extras = {}
            if 'extra_yamls' in values:
                for extra in values['extra_yamls']:
                    file = datafile(self.mode, extra)
                    with open(file, 'r') as f:
                        extras[extra] = yaml.safe_load(f)

            for testcase_name, content_values in content.items():
                if 'source' not in content_values:
                    log.info("'{tname}' is missing "\
                             "'source'".format(tname=testcase_name))
                    continue

                if content_values['source']['class'] ==\
                        'genie.harness.base.Template' and\
                    'cmd' in content_values:
                    source = content_values['cmd']
                else:
                    source = content_values['source']

                # Its possible a file exists there, but might not have the
                # actual name we want which is testcase_name.
                # Take the class and see what is there
                if 'class' not in source:
                    continue

                # We know the last value is name of the class
                path, cls = source['class'].rsplit('.', 1)
                if 'pkg' in source:
                    path = '{p}.{path}'.format(p=source['pkg'],path=path)

                module_loc = importlib.import_module(values['root'])
                root_dir = module_loc.__path__[0].split(
                    values['root'].replace('.', '/'))[0]
                extracted_package_path = module_loc.__path__[0].split(
                    values['mod_name'])[0]

                loc = path.replace('.', '/')
                loc = '{r}/{l}.py'.format(r=root_dir, l=loc)

                # Check if file exists
                if os.path.isfile(loc):
                    # Then check if this file has the right class
                    module = importlib.import_module(path)
                    cls_obj = getattr(module, cls, None)
                    if cls_obj:
                        # Found the non token version
                        if testcase_name not in self.output['testcases']:
                            self.output['testcases'].append(testcase_name)
                        if testcase_name not in self.output:
                            self.output[testcase_name] = {}

                        information = {}
                        if hasattr(cls_obj, '__description__'):
                            information['doc'] = cls_obj.__description__
                        else:
                            information['doc'] = cls_obj.__doc__
                        information['source_old'] = module.__file__

                        # if the trigger is from a user's contribution
                        if 'contrib' in information['source_old']:
                            information['contribute'] = True
                        else:
                            information['contribute'] = False

                        # Remove the package_path from the information['source']
                        package_path = self._expand(extracted_package_path)
                        temp_url = information['source_old'].replace(self.package_location + '/', '')
                        branch = values['url']['branch']
                        style = values['url']['style']

                        if style == 'bitbucket':
                            url = '{p}{t}{b}'.format(p=values['url']['link'], t=temp_url, b=branch)
                        elif style == 'github':
                            url = p=values['url']['link'].format(branch=branch)
                            url = '{p}{t}'.format(p=url, t=temp_url)

                        information['url'] = url
                        if hasattr(cls_obj, 'schema'):
                            #information['schema'] = json.dumps(str(cls_obj.schema), indent=2, sort_keys=True)
                            #information['schema'] = pprint.pformat(cls_obj.schema)
                            information['schema'] = format(cls_obj.schema)
                        information['source'] = content_values['source']
                        information.pop('source_old', None)
                        self.output[testcase_name]['top'] = information

                # it could be abstracted, so now trying to find it.
                # Every other directories are considered tokens
                # Path is the location of the Non token location
                # Including the name of the file
                # Got to remove the file, as we only want directory
                # But keep in memory, as it must match the file below
                path, file_name = path.rsplit('.', 1)
                try:
                    directories = next(os.walk(os.path.dirname(loc)))[1]
                except StopIteration as e:
                    continue

                for directory in directories:
                    # ignore directories in IGNORE_DIR or starting with dot, e.g. '.vscode'
                    if directory in self.IGNORE_DIR or directory[0] == '.':
                        continue
                    tokens = [directory]
                    full_path = os.path.join(os.path.dirname(loc), directory)
                    for dirname, subdir, files in os.walk(full_path, topdown=True):
                        subdir[:] = [s for s in subdir if s not in self.IGNORE_DIR]

                        tokens = tokens + self._find_diff(full_path.split('/'), dirname.split('/'))

                        # Get tokens
                        # Only keep tokens which exists in the dirname
                        toks = []
                        for tok in tokens:
                            if tok == 'n9kv' or tok == 'n9300':
                                toks.pop() if tok in toks else None
                            if tok in dirname and tok not in toks:
                                toks.append(tok)

                        # Is there a file containing our specific Trigger
                        new_path = '{p}.{t}'.format(p=path,
                                                    t='.'.join(toks))

                        for file in files:
                            if file != file_name + '.py':
                                continue

                            file_path = '{np}.{f}'.format(np=new_path,
                                                          f=file_name)

                            module = importlib.import_module(file_path)
                            cls_obj = getattr(module, cls, None)
                            if cls_obj:
                                # Found the/one of token version
                                if testcase_name not in self.output['testcases']:
                                    self.output['testcases'].append(testcase_name)
                                if testcase_name not in self.output:
                                    self.output[testcase_name] = {}
                                information = {}
                                if hasattr(cls_obj, '__description__'):
                                    information['doc'] = cls_obj.__description__
                                else:
                                    information['doc'] = cls_obj.__doc__
                                information['source'] = content_values['source']
                                if hasattr(cls_obj, 'schema'):
                                    #information['schema'] = json.dumps(str(cls_obj.schema), indent=2, sort_keys=True)
                                    #information['schema'] = pprint.pformat(cls_obj.schema)
                                    information['schema'] = format(cls_obj.schema)

                                # Remove the package_path from the information['source']
                                temp_url = module.__file__.replace(self.package_location + '/', '')

                                branch = values['url']['branch']
                                style = values['url']['style']

                                if style == 'bitbucket':
                                    url = '{p}{t}{b}'.format(p=values['url']['link'], t=temp_url, b=branch)
                                elif style == 'github':
                                    url = values['url']['link'].format(branch=branch)
                                    url = '{p}{t}'.format(p=url, t=temp_url)

                                information['url'] = url

                                # Add groups incase this trigger is not in the token trigger_datafile
                                information['groups'] = []

                                # Update self.output
                                temp_dict = self.output[testcase_name]
                                temp_hold = temp_dict
                                for token in toks:
                                    if token not in temp_dict:
                                        temp_dict[token] = {}
                                    temp_hold = temp_dict
                                    temp_dict = temp_dict[token]
                                    if token not in self.output['tokens']:
                                        self.output['tokens'].append(token)
                                self.output['tokens'] = sorted(self.output['tokens'])

                                # Get last token
                                temp_hold[token] = information

                # Now check the remaining yaml files and see if that trigger is
                # inside there but was not discovered within the directories
                for extra, extra_values in extras.items():
                    if testcase_name not in extra_values:
                        continue

                    if testcase_name not in self.output and self.type_ == 'verifications':
                        raise Exception("\n  The class used for '{testcase_name}' does not exist.\n"
                                        "  Most likely scenario is it was renamed without updating "
                                        "the verification_datafiles.".format(testcase_name=testcase_name))

                    # If testcase was already added from token discovery,
                    # add all extra values
                    if extra in self.output[testcase_name]:
                        self.output[testcase_name][extra].update(extra_values[testcase_name])
                        self.output[testcase_name][extra].setdefault('groups', [])
                        continue

                    # Verifications should never reach this point.
                    # If it does then the verification datafile (os specific) contains
                    # verifications it shouldn't. Such as pointing to a parser that
                    # doesnt exist for an os (extra)
                    if self.type_ == 'verifications':
                        raise Exception("\n  The {os} verification_datafile cannot have '{testcase_name}'.\n"
                                        "  Details: The parser used by '{testcase_name}' does not exist for {os}\n"
                                        .format(os=extra, testcase_name=testcase_name))

                    # Then add the os for that testcase, but no __doc__
                    # And same source as the top one
                    information = {}
                    information['doc'] = ''
                    information['source'] = self.output[testcase_name]['top']['source']
                    information.update(extra_values[testcase_name])
                    information.setdefault('groups', [])

                    if 'contrib' in information['source']:
                        information['contribute'] = True
                    else:
                        information['contribute'] = False
                    # Remove the package_path from the information['source']
                    try:
                        temp_url = information['source_old'].replace(self.package_location + '/', '')
                    except KeyError:
                        pass
                    branch = values['url']['branch']
                    style = values['url']['style']

                    if style == 'bitbucket':
                        url = '{p}{t}{b}'.format(p=values['url']['link'], t=temp_url, b=branch)
                    elif style == 'github':
                        url = values['url']['link'].format(branch=branch)
                        url = '{p}{t}'.format(p=url, t=temp_url)

                    if extra not in self.output['tokens']:
                        self.output['tokens'].append(extra)

                    information['url'] = url
                    self.output[testcase_name][extra] = information

                self.output['tokens'] = sorted(self.output['tokens'])


def _worker(payload):
    # Unpack payload
    maker, save_file = payload

    maker.make()

    # Create file and save maker output
    os.makedirs(os.path.dirname(save_file), exist_ok=True)
    with open(save_file, 'w+') as f:
        f.write(json.dumps(maker.output,
                           sort_keys=True,
                           indent=2,
                           separators=(',', ': ')))

def make_genieparser():
    payloads = []

    # Gathering required payloads for genieparser
    for k, v in list(DATAFILES['parsers'].items()):
        payloads.append((MakeParsers(k), v))

    # Spinning up one child process per payload
    pcall(_worker, payload=payloads)

def make_genielibs():
    payloads = []

    # Gathering required payloads for genielibs
    for k, v in list(DATAFILES['apis'].items()):
        payloads.append((MakeApis(k), v))

    for k, v in list(DATAFILES['ops'].items()):
        payloads.append((MakeOps(k), v))

    for k, v in list(DATAFILES['clean'].items()):
        payloads.append((MakeClean(k), v))

    for k, v in list(DATAFILES['models'].items()):
        payloads.append((MakeModels(k), v))

    for k, v in list(DATAFILES['triggers'].items()):
        payloads.append((MakeTriggersVerifications(k, 'triggers'), v))

    for k, v in list(DATAFILES['verifications'].items()):
        payloads.append((MakeTriggersVerifications(k, 'verifications'), v))

    # Spinning up one child process per payload
    pcall(_worker, payload=payloads)

def make_genie():
    """
    This function remains for backwards compatibility. The json files for 
    models, triggers, and verifications have all been moved to genielibs, but
    leaving this so `make json` in genie repo still updates those 3 json files
    """
    payloads = []

    # Gathering required payloads for genie
    for k, v in list(DATAFILES['models'].items()):
        payloads.append((MakeModels(k), v))

    for k, v in list(DATAFILES['triggers'].items()):
        payloads.append((MakeTriggersVerifications(k, 'triggers'), v))

    for k, v in list(DATAFILES['verifications'].items()):
        payloads.append((MakeTriggersVerifications(k, 'verifications'), v))

    # Spinning up one child process per payload
    pcall(_worker, payload=payloads)

def make_all():
    payloads = []

    # Gathering required payloads for genieparser
    for k, v in list(DATAFILES['parsers'].items()):
        payloads.append((MakeParsers(k), v))


    # Gathering required payloads for genielibs
    for k, v in list(DATAFILES['apis'].items()):
        payloads.append((MakeApis(k), v))

    for k, v in list(DATAFILES['ops'].items()):
        payloads.append((MakeOps(k), v))

    for k, v in list(DATAFILES['clean'].items()):
        payloads.append((MakeClean(k), v))


    # Gathering required payloads for genie
    for k, v in list(DATAFILES['models'].items()):
        payloads.append((MakeModels(k), v))

    for k, v in list(DATAFILES['triggers'].items()):
        payloads.append((MakeTriggersVerifications(k, 'triggers'), v))

    for k, v in list(DATAFILES['verifications'].items()):
        payloads.append((MakeTriggersVerifications(k, 'verifications'), v))

    # Spinning up one child process per payload
    pcall(_worker, payload=payloads)
