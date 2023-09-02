# importlib
import re
import importlib
from collections import deque

# Lookup
from genie.abstract import Lookup


def load_attribute(pkg, attr_name, device=None):
    # a pkg is used for abstraction, as the package has to be imported
    # first

    if pkg:
        # Get package name
        pkg_name = pkg.split('.')[-1]
        # import it; if it explodes,  then it will error
        attribute = importlib.import_module(name=pkg)
        if getattr(attribute, '__abstract_pkg', None):
            # Lookup is cached,  so only the first time will be slow
            # Otherwise it is fast
            attribute = Lookup.from_device(device,
                                           packages={pkg_name:attribute})
            # Build the class to use to call
            items = attr_name.split('.')
            items.insert(0, pkg_name)
        else:
            items = attr_name.split('.')

        for item in items:
            try:
                attribute = getattr(attribute, item)
            except LookupError as e:
                if 'abstraction package' in str(e):
                    # then could not find the abstracted package
                    raise LookupError('Could not find {}.{} for device {}'
                                      .format(pkg, attr_name, device.name))
            except Exception as e:
                pass
    else:
        # So just load it up
        module, attr_name = attr_name.rsplit('.', 1)

        # Load the module
        mod = importlib.import_module(module)

        # Find the right attribute
        try:
            attribute = getattr(mod, attr_name)
        except AttributeError as e:
            raise AttributeError("Couldn't find '{name}' in "
                                 "'{mod}'".format(name=attr_name,
                                                  mod=mod)) from e
    return attribute

def str_to_list(string):
    reg = re.findall('\(.*?\)', string)
    # Remove it from src and keep track of the position
    reg_src = {}
    reg_space = {}
    if reg:
        for reg_item in reg:
            reg_src[string.find(reg_item)] = reg_item
            string = string.replace(reg_item, ' ' * len(reg_item), 1)

    # Another corner case; if any of the variable has space into them
    # got to remove those too and add to reg_src
    reg = re.findall('[\(\w\)]+\s+[\(\w)\)]+.*?]', string)
    if reg:
        for reg_item in reg:
            reg_item = reg_item.replace(']', '')
            new_item = reg_item.replace(' ', '~')
            reg_space[new_item] = reg_item
            string = string.replace(reg_item, new_item)

    string = string.replace('[', ' ').replace(']', ' ')

    # Now put it back
    if reg_src:
        for key, value in reg_src.items():
            string = string[:key] + value + string[key+len(value):]
    ret_list = string.split()

    # Now go put back the reg_space and ~
    new_ret = deque()
    for i, item in enumerate(ret_list):
        if item in reg_space:
            item = reg_space[item]
        if '~' in item:
            item = item.replace('~', ' ')
        try:
            item = int(item)
        except Exception:
            pass
        new_ret.append(item)
    return new_ret

def structure_verifier(string, data):
    keys = str_to_list(string)
    for key in keys:

        # Regex
        if key.startswith('('):

            try:
                com = re.compile(key)
            except Exception as e:
                raise ValueError("'{key}' is not a valid regex "
                                 "expression".format(key=key)) from e

            # This is ONLY valid if com.pattern is .*
            if com.pattern == '(.*)':
                continue
            else:
                break
