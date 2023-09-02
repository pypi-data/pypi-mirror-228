# python
import os
from copy import deepcopy
import json
import logging
import inspect
import weakref
import pathlib
import importlib
from collections import OrderedDict
from pkg_resources import iter_entry_points
import re

# pyATS
from pyats.log.utils import banner
from pyats.aetest.steps import Steps
from pyats import configuration as cfg
from pyats.utils.dicts import recursive_update
from pyats.utils.yaml import markup
from pyats.utils.yaml.exceptions import MarkupError

# Genie
from genie.utils import Dq
from genie.libs.sdk import apis
from genie.abstract import Lookup
from genie.json.make_json import MakeApis
from genie.metaparser.util import merge_dict
from genie.metaparser.util.schemaengine import Schema
from .utils import prune_if

API_PLUGIN_ENTRYPOINT = 'genie.libs.sdk.apis'
PYATS_EXT_API = 'pyats.libs.external.api'

# sentinel values
class TO_DELETE: pass
class OPTIONAL: pass
class REQUIRED: pass


log = logging.getLogger(__name__)

function_data = None

try:
    from genie.libs.cisco.telemetry import add_api_usage_data
    INTERNAL = True
except:
    INTERNAL = False


class ExtendApis(MakeApis):
    def __init__(self, package):
        self.output = {'tokens': [], 'extend_info': []}
        self.package = package
        self.root = {
            'root': package,
            'mod_name': 'apis',
            'url': {
                'link':
                'https://github.com/CiscoTestAutomation/genielibs/tree/{branch}/',
                'branch': 'master',
                'style': 'github',
            },
        }
        self.module_loc = importlib.import_module(package).__path__[0]
        self.package_location = self.module_loc

    def extend(self):
        """ Recursively find the api in the external genie api package
            and store the information into self.output dictionary """
        self._recursive_find(pathlib.Path(self.module_loc), [])


def _load_function_json():
    """get all api data in json file"""

    try:
        mod = importlib.import_module("genie.libs.sdk.apis")
        functions = os.path.join(mod.__path__[0], "apis.json")
    except Exception:
        functions = ""

    if not os.path.isfile(functions):
        log.warning("apis.json does not exist, make sure you "
                    "are running with latest version of "
                    "genie.libs.sdk")
        function_data = {}
    else:
        # Open all the apis in json file
        with open(functions) as f:
            try:
                function_data = json.load(f)
            except json.decoder.JSONDecodeError:
                log.error(
                    banner(
                        "api json file could be corrupted. Please try 'make json'"
                    ))
                raise

        # check if provided external api package from pyats.conf
        # if provided then extend genie api json file with
        # external package data
        ext_api_package = cfg.get(PYATS_EXT_API, None) or \
            os.environ.get(PYATS_EXT_API.upper().replace('.', '_'))

        entrypoint_packages = [
            entrypoint.module_name
            for entrypoint in iter_entry_points(group=API_PLUGIN_ENTRYPOINT)
        ]

        if ext_api_package:
            api_packages = set([ext_api_package] + entrypoint_packages)
        else:
            api_packages = entrypoint_packages

        for api_package in api_packages:
            ext = ExtendApis(api_package)

            ext.extend()

            ext.output.pop('tokens', None)
            summary = ext.output.pop('extend_info', None)

            log.debug("API count from {}: {}".format(api_package,
                                                     len(summary)))
            log.debug('APIs:\n{}'.format(json.dumps(summary, indent=4)))
            # merge the original api data with external api data
            merge_dict(function_data, ext.output, update=True)

    return function_data


class API(object):
    def __init__(self, device=None):
        global function_data

        self.clean = CleanAPI(device)

        # list of apis which had error to load
        self.error_modules = []

        self.device = weakref.ref(device) if device else device
        if function_data is None:
            self.function_data = _load_function_json()
            function_data = self.function_data
        else:
            self.function_data = function_data

    def __getstate__(self):
        return vars(self)

    def __getattr__(self, name):
        def wrapper_match(*args, **kwargs):

            device = self.device() if self.device else self.device

            original_alias = ''
            # check if 'alias' argument is passed
            if 'alias' in kwargs:
                connection_alias = kwargs['alias']
                # check if given alias exists in connectionmgr
                if connection_alias in device.connectionmgr.connections:
                    original_alias = device.connectionmgr.connections._default_alias
                    # overwrite _default_alias temporarily
                    device.connectionmgr.connections._default_alias = connection_alias
                    log.debug(
                        f"Changed from default alias '{original_alias}' to '{connection_alias}'."
                    )
                else:
                    log.warning(
                        f"given connection alias '{connection_alias}' doesn't exist in connections. so use default alias '{device.connectionmgr.connections._default_alias}'"
                    )

            try:
                func = self.get_api(name, device)

                # if the function does not take a device, just return it
                # or device is already in kwargs
                func_args = inspect.getfullargspec(func)
                if original_alias and 'alias' not in func_args.args:
                    kwargs.pop('alias')
                if 'device' in func_args.args and 'device' not in kwargs:
                    # Then add to positional arguments
                    index = func_args.args.index('device')
                    args = args[:index] + (device, ) + args[index:]

                func_result = func(*args, **kwargs)
            except Exception:
                raise
            finally:
                if original_alias:
                    # change _default_alias back to original one
                    device.connectionmgr.connections._default_alias = original_alias
                    log.debug(
                        f"Changed back from {connection_alias} to default alias '{original_alias}'."
                    )

            return func_result

        return wrapper_match

    def __dir__(self):
        device = self.device() if self.device else self.device
        return self.get_all_api(device)

    def get_all_api(self, device=None):
        # set ensures no duplicate elements
        result = set()

        # if no device provided, only return common ones
        if not device:
            for api, keys in self.function_data.items():
                if 'com' in keys:
                    result.add(api)
            return result

        lookup = Lookup.from_device(device, packages={"apis": apis})

        for name, data in self.function_data.items():
            for token in lookup._tokens:
                # if this api support the token, add
                if token in data:
                    result.add(name)
                    break
            # does not support token but has 'com' key, also add
            else:
                if 'com' in data:
                    result.add(name)
        return sorted(result)

    def get_api(self, api_name, device=None):
        """From a api function and device, return the function object"""

        try:
            data = self.function_data[api_name]
        except KeyError:
            raise AttributeError("Could not find an API called '{c}'".format(
                c=api_name)) from None

        # if missing device, then it must be under com
        if device is None:
            return getattr(
                self._get_submodule(apis, data['com']["module_name"]),
                api_name)

        try:
            lookup = Lookup.from_device(device, packages={"apis": apis})
        except Exception as err:
            # Adds the module name to 'error_modules' list
            if err.absname:
                self.error_modules.append(err.absname)

        # If there is an error the module with error will be reloaded
        # to show the same error and do the lookup on it
        if self.error_modules:
            for errored_apis_modules in self.error_modules:
                importlib.import_module(errored_apis_modules)
            # if import is successfull, we reach below code.
            # Reloading the APIs and creating a new lookup object
            # to make sure the have the proper data.
            importlib.reload(apis)
            lookup = Lookup.from_device(device, packages={"apis": apis})
            self.error_modules = []

        iterated_data = data
        # find the API in the lowest level of the json tokens
        for token in lookup._tokens:
            if token in iterated_data:
                iterated_data = iterated_data[token]
            else:
                break

        # Now that we know the API is valid, try to add API to telemetry data
        if INTERNAL:
            try:
                add_api_usage_data(api_name, iterated_data, device)
            except Exception as e:
                log.debug(
                    "An error occurred while adding API to telemetry data."
                    " Error: %s" % str(e))

        # Try to load it
        try:
            package = iterated_data.get('package')
            if package:
                # in case external lookup package
                new_lookup = Lookup.from_device(
                    device,
                    packages={'apis': importlib.import_module(package)})
            else:
                new_lookup = lookup
            api_function = getattr(
                self._get_submodule(new_lookup.apis,
                                    iterated_data["module_name"]), api_name)
        except Exception:
            pass
        else:
            return api_function

        # Last resort, check under 'com' token
        try:
            package = data['com'].get('package')
            if package:
                # in case external lookup package
                new_lookup = Lookup.from_device(
                    device,
                    packages={'apis': importlib.import_module(package)})
            else:
                # default lookup package
                new_lookup = lookup
            api_function = getattr(
                self._get_submodule(new_lookup.apis,
                                    data["com"]["module_name"]), api_name)
        except Exception:
            raise AttributeError(
                "Could not find the API under {o}, and common".format(
                    o=lookup._tokens)) from None
        else:
            return api_function

    def _get_submodule(self, abs_mod, mods):
        """recursively find the submodule"""
        if "." not in mods:
            return getattr(abs_mod, mods)
        current, next = mods.split(".", 1)
        mod = getattr(abs_mod, current)
        try:
            return getattr(mod, next)
        except Exception:
            pass
        return self._get_submodule(mod, next)


class CleanArgProcessor(markup.Processor):
    """
    Used to substitute clean args provided by the user into the clean template
    """

    CLEAN_ARG_PATTERN = re.compile(r"(%CLEANARG{ *(.*?) *})")

    def match_cleanarg_markup(self, data):
        """
        Method which returns whether or not `data` arg contains %CLEANARG{}
        placeholder
        """
        return self.CLEAN_ARG_PATTERN.search(data)

    def process_cleanarg_markup(self, match, data, index, locations=None):
        """
        Action to perform when %CLEANARG{} placeholder is found (substitute
        the corresponding value stored in our clean_args attribute)
        """
        if not match:
            return data

        key = match.group(2)
        if self.clean_args_allow_missing:
            value = self.clean_args.get(key, "")
        else:
            try:
                value = self.clean_args[key]
            except KeyError as e:
                raise TypeError(f"Required clean argument '{key}' not provided") from e

        if not isinstance(value, str):
            return value

        # do replacement
        data = data.replace(data[slice(*match.span(0))], str(value))
        return data

    def __init__(self, *args, clean_args={}, allow_missing=False, **kwargs):
        """
        Initialize parent class and register actions for %CLEANARG{} placeholder

        clean_args: key-value data. When we find a %CLEANARG{} placeholder we
        will look up the corresponding value for the argument here. e.g. if
        we find %CLEANARG{foo} and clean_args={"foo": "bar"} then %CLEANARG{foo}
        gets replaced by bar

        allow_missing: if False then raise exception if key not found in clean_args.
        If True then an empty string is used if key not found
        """
        super().__init__(*args, **kwargs)
        self.clean_args = deepcopy(clean_args)
        self.clean_args_allow_missing = allow_missing
        self._actions.append((self.match_cleanarg_markup,
                              self.process_cleanarg_markup))


class CleanAPI(object):

    def __init__(self, device=None):
        self.device = self.device = weakref.ref(device) if device else device
        self.history = OrderedDict()

    @property
    def arguments(self):
        template = self.template

        stages = {}
        for stage in template.get('order', []):
            schema = self.__getattr__(stage).schema

            stages[stage] = self._generate_stage_arguments(schema)

        return stages

    def _generate_stage_arguments(self, schema):
        args = {}

        for argument in schema:

            if isinstance(argument, Schema):
                arg_name = argument.schema
            else:
                arg_name = argument

            if isinstance(schema[argument], dict):
                args[arg_name] = self._generate_stage_arguments(schema[argument])
            else:
                args[arg_name] = {}
                args[arg_name].update({'type': schema[argument]})

                if hasattr(argument, 'description') and argument.description is not None:
                    args[arg_name].update({'description': argument.description})

                # todo: arguments set in the template should overwrite the defaults in the stage class
                if hasattr(argument, 'default') and argument.default != 'n/a':
                    args[arg_name].update({'default': argument.default})

        return args

    @property
    def template(self):
        return self.get_template("DEFAULT")

    def get_template(self, template_name):
        """
        clean package has an abstract module templates.py. Using the device,
        lookup the variable with name `template_name` in templates.py
        """
        if template_name != template_name.upper():
            raise TypeError(f"Expected upper case template name. Got '{template_name}'")

        # Due to circular import
        from genie.libs.clean.utils import get_clean_template

        device = self.device() if self.device else self.device

        try:
            return get_clean_template(device, template=template_name)
        except LookupError as e:
            raise LookupError(f"Clean template '{template_name}' not found for {device.os}/{device.platform}") from e

    def get_template_args(self, template_name):
        """
        Lookup default arguments for the template

        for example, if template_name is 'MY_TEMPLATE' then we use pyats
        abstraction mechanism to lookup a variable called 'MY_TEMPLATE_ARGS'.
        This is expected to be a dictionary of default values for substitutions
        into 'MY_TEMPLATE' variable (can be an empty dict if there are no default args)
        """
        if template_name != template_name.upper():
            raise TypeError(f"Expected upper case template name. Got '{template_name}'")

        # arguments are expected to follow this format
        template_args_name = f"{template_name}_ARGS"

        # Due to circular import
        from genie.libs.clean.utils import get_clean_template

        device = self.device() if self.device else self.device

        try:
            return get_clean_template(device, template=template_args_name)
        except LookupError:
            return {}

    def render_clean_template(self, template_name="DEFAULT", template_override={}, template=None, clean_args={}):
        """
        at a high level, this function does the following:
        1. look up the "default arguments" for the template and merge in any
        overrided values provided by user (clean_args)
        2. look up the template and merge in an overrides from user (template_override)
        3. use markup processor to substitute arguments into template (template can have
        placeholders with form %CLEANARG{...})
        4. prune any "unresolved" optional fields after rendering, and ensure
        that any required fields exist after rendering is complete
        """
        # circular dependency
        from genie.libs.clean.clean import NOT_A_STAGE

        template_data = {}
        template_args = {}
        if template_name is not None:
            template_data = deepcopy(self.get_template(template_name))
            template_args = deepcopy(self.get_template_args(template_name))

        recursive_update(template_data, deepcopy(template_override))
        recursive_update(template_args, deepcopy(clean_args))

        # overwrite template with given template
        if template:
            template_data = template

        # resolve "order" so we can figure out if some stages can be removed
        # from the template (this way when we invoke CleanArgProcessor with
        # allow_missing==False, we wont be required to provide arguments
        # for stages which wont be executed)
        pre_arg_processor = CleanArgProcessor(clean_args=template_args, allow_missing=True)
        tmp = pre_arg_processor(deepcopy(template_data))
        order = tmp.get("order", [])
        kept_stages = {s for s in order}
        kept_stages.update(NOT_A_STAGE)
        removed_stages = template_data.keys() - kept_stages
        if removed_stages:
            log.debug(f"removing unused stages {removed_stages}")
            for s in removed_stages:
                del template_data[s]

        arg_processor = CleanArgProcessor(clean_args=template_args, allow_missing=False)

        try:
            rendered_data = arg_processor(deepcopy(template_data))
        except MarkupError as e:
            # markup processor wraps the exception. Unwrap it to give
            # more informative exception to user
            log.exception(f"Error substituting args={template_args}"
                          f" into clean template={template_data}")
            if e.__cause__:
                raise e.__cause__
            raise e

        # any fields still equal to OPTIONAL are optional arguments
        # which user didnt provide. We can delete them
        prune_if(rendered_data, lambda v: v == OPTIONAL)

        # user has indicated the field should be deleted
        prune_if(rendered_data, lambda v: v == TO_DELETE)

        def raise_required_missing(v):
            if v == REQUIRED:
                raise TypeError("REQUIRED argument not provided")
            return False

        try:
            # we are using prune_if to iterate/walk over the
            # data and call raise_required_missing. So we arent
            # really using it to "prune" anything here
            prune_if(rendered_data, raise_required_missing)
        except TypeError:
            raise TypeError(
                f"Some required clean arguments not provided: {template_args}."
                f" Incomplete template: {rendered_data}."
            )

        return rendered_data

    def __getattr__(self, stage_name):
        """ Returns an initialized clean stage object """
        device = self.device() if self.device else self.device

        log.debug(f"Retrieving stage '{stage_name}' for {device.name} "
                  f"(OS:{device.os}, PLATFORM:{device.platform})")

        if (stage_name in device.clean and
                'source' in device.clean[stage_name]):

            # Due to circular import
            from genie.harness.utils import load_class

            # Load the clean stage class from the provided source
            stage_cls = load_class(device.clean[stage_name], device)
        else:
            # Due to circular import
            from genie.libs.clean.utils import load_clean_json, get_clean_function

            # Load the clean stage class from the clean.json file
            stage_cls = get_clean_function(stage_name, load_clean_json(), device)

        stage = stage_cls()
        stage.__name__ = stage.__uid__
        stage.history = self.history
        stage.history[stage.uid] = stage

        # Default the mandatory params. These can be overwritten when the
        # user calls the stage with arguments
        stage.parameters.update({
            'device': device,
            'steps': Steps()
        })

        return stage

    def __call__(self, template_name="DEFAULT", template_override={}, template=None, **kwargs):
        """
        Renders the clean template and uses it to call clean

        The genie clean package has an abstract module called templates.py,
        which is looked up according to device os,platform,model

        In templates.py there are clean templates. A clean template is JSON
        data which can have placeholders for data which the user needs to
        provide when calling this API. Similar to how Python functions
        can have keyword arguments with default values, default arguments
        may also be defined for a clean template. These are stored in
        a Python dictionary whose variable name should follow this
        convention: {template_name}_ARGS

        Shortened example:

        ```python
        from genie.conf.base.api import OPTIONAL, REQUIRED

        MY_TEMPLATE = {
            "order": [
                "connect",
                "apply_configuration",
                "ping_server",
                "copy_to_device",
            ],
            "images": r"%CLEANARG{images}",
            "connect": {},
            "apply_configuration": {
                "configuration": r"%CLEANARG{config_str}",
            },
            "ping_server": {
                "server": "%CLEANARG{server}",
                "vrf": "%CLEANARG{vrf}",
            },
            "copy_to_device": {
                "overwrite": r"%CLEANARG{overwrite}",
                "origin": {
                    "hostname": "%CLEANARG{server}",
                },
                "vrf": "%CLEANARG{vrf}",
            },
        }

        MY_TEMPLATE_ARGS = {
            "vrf": "management",    # argument with default which user can override
            "server": REQUIRED,     # required argument which user must provide
            "overwrite": OPTIONAL,  # optional argument
            "config_str": REQUIRED,
            "images": REQUIRED,
        }
        ```

        Arguments:
        1. template_name: which clean template to use, or None to not use any
        clean template

        2. template_override: optionally override data in clean template. This
        is done with a recursive dictionary update. Example:

        ```python
        # template assumes config string is being provided. We want
        # to use a config file

        config_file_location = "..."
        override = {"apply_configuration": {"file": config_file_location}}
        dev.api.clean(template_name="MY_TEMPLATE", template_override=config_file_location)
        ```

        3. kwargs: arguments which are substituted into the template. Example:

        ```python
        dev.api.clean(
            template_name="MY_TEMPLATE",
            vrf="Mgmt",
            server="10.10.10.10",
            images={
                "server": [...],
                "kickstart": [...],
            }
            ...
        )
        ```

        vrf, server and config_str are all kwargs, and will be substituted into
        the MY_TEMPLATE template to render the clean YAML that is used when
        invoking clean

        TODO: some warning logs if a provided kwarg doesnt end up
        being used for anything?
        """

        device = self.device() if self.device else self.device

        # save whatever is under device.clean for restoring
        orig_clean = device.clean

        clean_data = self.render_clean_template(template_name=template_name,
                                                template_override=template_override,
                                                template=template,
                                                clean_args=kwargs)

        log.debug(f"calling clean with {clean_data}")

        # circular dependency
        from genie.libs.clean import PyatsDeviceClean

        try:
            device.clean = clean_data
            # Run the clean template
            PyatsDeviceClean().clean(device)
        except Exception:
            raise
        finally:
            # restore device.clean
            device.clean = orig_clean

    def __dir__(self):
        device = self.device() if self.device else self.device

        # Due to circular import
        from genie.libs.clean.utils import load_clean_json

        clean_json = load_clean_json()
        tokens = Lookup.tokens_from_device(device)

        # Get all stages for this device
        stages = []
        for stage, data in clean_json.items():

            # tokens isn't a stage so ignore it
            if stage == 'tokens':
                continue

            data = Dq(data)
            for token in tokens:

                # If the 'uid' key is found under any of the device abstraction
                # tokens or the 'com' token, then the stage is supported.
                if (data.contains_key_value(token, 'uid') or
                        data.contains_key_value('com', 'uid')):
                    stages.append(stage)
                    break

        return super().__dir__() + stages
