import pathlib
import importlib
from genie.json.make_json import MakeClean as GenieMakeClean


class ExtendClean(GenieMakeClean):

    def __init__(self, package):
        self.output = {'tokens': []}
        self.package = package
        self.root = {
            'root': package,
            'mod_name': 'clean',
            'url': {
                'link': 'https://wwwin-github.cisco.com/pyATS/genielibs.cisco/tree/{branch}/',
                'branch': 'dev',
                'style': 'github',
            },
        }
        self.module_loc = importlib.import_module(package).__path__[0]
        self.package_location = self.module_loc

    def extend(self):
        """ Recursively find the clean stages in the external package
            and store the information into self.output dictionary """
        self._recursive_find(pathlib.Path(self.module_loc), [])
