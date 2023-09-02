import importlib
import json
import logging
import os
from pyats.utils.yaml.loader import Loader


log = logging.getLogger(__name__)


def _get_json(arg):
    """get all json data"""

    jsons_dict = {
        'parsers': {
            'module': 'genie.libs.parser',
            'file': 'parsers.json',
        },
        'ops': {
            'module': 'genie.libs.ops',
            'file': 'ops.json',
        },
        'triggers': {
            'module': 'genie.libs.sdk.triggers',
            'file': 'triggers.json',
        },
        'verifications': {
            'module': 'genie.libs.sdk.verifications',
            'file': 'verifications.json',
        },
        'apis': {
            'module': 'genie.libs.sdk.apis',
            'file': 'apis.json',
        }
    }

    # Look up module's path and file's name in the dictionary
    if arg in jsons_dict:
        mod_path = jsons_dict[arg]['module']
        file_name = jsons_dict[arg]['file']
    else:
        raise Exception('{arg} is not a valid type.'.format(arg=arg))

    mod = importlib.import_module(mod_path)
    functions = os.path.join(mod.__path__[0], file_name)

    if not os.path.isfile(functions):
        log.warning(
            "{file_name} does not exist, make sure you "
            "are running with latest version of "
            "{mod_path}"
        ).format(file_name=file_name, mod_path=mod_path)
        function_data = {}
    else:
        # Load the Json file and return the content
        with open(functions) as f:
            function_data = json.dumps(json.load(f))
    return function_data


def get_parsers_json():
    return _get_json('parsers')


def get_ops_json():
    return _get_json('ops')


def get_triggers_json():
    return _get_json('triggers')


def get_verifications_json():
    return _get_json('verifications')


def get_apis_json():
    return _get_json('apis')


def yaml_to_json(paths):
    """ takes multiple yaml files and converts to json

        Args:
            paths ('str'): path to yaml file(s) seperated by ':'
                ex: '/path/to/yaml.yaml:/path/to/another/yaml.yaml'
    """
    if not paths:
        return json.dumps({})

    yaml = Loader(enable_extensions=True)
    ret = {}

    for path in paths.split(":"):

        data = yaml.safe_load(path)

       # Using com as we dont know what OS it comes from
        for key in list(data):
            data[key] = {'com': data[key]}

        ret.update({path:data})

    return json.dumps(ret)

