import re
import logging
from .exceptions import (SchemaValueError, SchemaClassError, SchemaTypeError,
                          SchemaMissingKeyError, SchemaUnsupportedKeyError,
                          SchemaError, SchemaFallbackError,
                          SchemaFallbackLoopError, SchemaEmptyParserError,
                          SchemaFallbackCall)

from pyats.datastructures import ListDict


log = logging.getLogger(__name__)


class Schema(object):
    '''Schema class

    Provides the ability to define schema (schematics/requirements) for input
    data, and subsequently validate whether the input data meets requirements.

    Example:
        data = Schema(str).validate('a string')
        data = Schema({'a': str}).validate({'a': 'some string'})

    Arguments:
        schema (*): the schema to be validated against. Any valid python
                    datastructures/callable.
        description (str, optional): A string to describe the key in more detail.
        default (str, optional): To pass a default value to the key.

    See Also:
        PyPI: schema https://pypi.python.org/pypi/schema/0.3.1
    '''
    def __init__(self, schema, path=None, description=None, default='n/a'):
        self.schema = schema
        self.schemaType = type(schema)
        self.missed = []
        self.description = description
        self.default = default

        if not path:
            self.path = []
        else:
            self.path = path.copy()

    def __str__(self):
        return "{class_name} {path} {schema_type} {schema}".format(
            class_name = self.__class__.__name__,
            path = '.'.join([str(i) for i in self.path]),
            schema_type = "({})".format(self.schemaType.__name__),
            schema = self.schema)

    def __repr__(self):
        return self.__str__()

    @classmethod
    def priority(self, obj):
        '''Function to make sure that we always process Any objects last.

        Eg. process mandatory and optional ones first before trying to match
        Any'''
        if isinstance(obj, Any):
            return 3
        elif isinstance(obj, Optional):
            return 2
        else:
            return 1

    def collect_defaults(self):
        '''collect_defaults

        Based on the given schema, compute the defaults, if any. This involves
        using the Default subclass and creating a new datastructure that 
        represents the default state of this schema (eg, with a None input,
        the resulting data should look like the output of this)

        '''
        if issubclass(self.schemaType, dict):
            defaults = ListDict()
            for path, obj in ListDict(self.schema):
                if isinstance(obj, Default):
                    defaults.append((path, obj.validate(None)))
            return defaults.reconstruct()
        elif issubclass(self.schemaType, Default):
            return self.schema.validate(None)
        else:
            return None

    def collect_fallbacks(self):
        '''collect_fallbacks

        Based on the given schema, compute the fallbacks, if any. This involves
        using the Fallback subclass and creating a new datastructure that 
        represents the fallback states of this schema, eg, if a key does not
        exist, it should fallback to another key's value.

        Note:
            Fallbacks are only valid if the schema type is Dict.

        '''
        if issubclass(self.schemaType, dict):
            fallbacks = ListDict()
            for path, obj in ListDict(self.schema):
                if isinstance(obj, Fallback):
                    if obj.fallback == path:
                        raise SchemaFallbackLoopError(obj.fallback, path)
                    fallbacks.append((path, obj))

            while True:
                # check if there are fallbacks falling back to fallbacks
                paths = [i for i, j in fallbacks]
                objs = [j for i, j in fallbacks]
                fallback_paths = [j.fallback for i, j in fallbacks]

                if not set(paths) & set(fallback_paths):
                    # all fallbacks are unique
                    break

                for obj in objs:
                    if obj.fallback in paths:
                        index = paths.index(obj.fallback)
                        if obj.fallback == objs[index].fallback:
                            # detect infinite loops
                            raise SchemaFallbackLoopError(obj.fallback,
                                                         paths[objs.index(obj)])
                        obj.fallback = objs[index].fallback

            return fallbacks.reconstruct()
        elif issubclass(self.schemaType, Fallback):
            return self.schema
        else:
            return None

    def apply_defaults(self, data):
        '''apply_defaults

        This API takes the current data and apply default fields to it wherever
        needed (eg, missing fields)

        Arguments:
            data (any): input data

        Returns:
            input data augmented with default values

        '''
        default = self.collect_defaults()

        if data is None:
            data = default
        elif isinstance(default, dict):
            default = ListDict(default)
            data = ListDict(data)
            paths = [Path(i) for i, j in data]

            for path, obj in default:
                # take into account that a path could be Any(), so convert 
                # a dict path to Path Object for comparisons
                path_obj = Path(path)
                #if path_obj not in paths:
                if path_obj.is_dynamic():
                    # add this to all respective path, including Any()
                    for missing_paths in path_obj.missing_from(paths):
                        data.append((missing_paths, obj))
                else:
                    if path_obj not in paths:
                        data.append((path, obj))

            data = data.reconstruct()

        return data

    def apply_fallback(self, data):
        '''apply_fallback

        This API goes through the schema looking for fallback fields. When
        found, it takes the fallback key, pull up its data, and apply it to
        the current field, if it doesn't exist.

        Arguments:
            data (any): input data

        Returns:
            input data augmented with fallback values
        '''
        fallback = self.collect_fallbacks()

        # note that fallback only works for dictionary types
        if fallback:
            fallback = ListDict(fallback)
            data = ListDict(data)
            paths = [i for i, j in data]
            path_objs = [Path(i) for i, j in data]

            for path, obj in fallback:
                # take into account that a path could be Any(), so convert 
                # a dict path to Path Object for comparisons
                path_obj = Path(path)
                try:
                    index = paths.index(obj.fallback)
                except ValueError:
                    raise SchemaFallbackError(obj.fallback, 
                                              data.reconstruct())
                if path_obj.is_dynamic():
                    for missing_paths in path_obj.missing_from(paths):
                        data.append((missing_paths, data[index][1]))
                else:
                    if path_obj not in path_objs:
                        data.append((path, data[index][1]))

            data = data.reconstruct()

        return data

    def validate(self, data, top=True, command='', warn_unsupported_keys=False):
        '''validate input

        Validates the given data against the current schema, and returns the
        correct, validated data. If there are defaults & fallbacks associated
        with the schema, augment the input data with them so that the final
        return contains validated data + the defaults/fallbacks.

        Arguments:
            data (any): data to be validated
            warn_unsupported_keys (bool): Log warning instead of raising an
                                          exception when unsupported keys
                                          are found.

        Returns:
            Validated data with defaults & fallbacks applied
        '''
        if not data and top is True:
            raise SchemaEmptyParserError(data, command)

        if top:
            # top is only true when user calls validate
            # this allows processing of defaults & follow fallbacks
            # as they change the actual input data
            data = self.apply_defaults(data)
            data = self.apply_fallback(data)

        # any matches any
        if issubclass(self.schemaType, Any):
            return data

        # if it is a subclass then evaluate it.
        if issubclass(self.schemaType, Schema):
            return self.schema.validate(data, False, command=command,
                                        warn_unsupported_keys=warn_unsupported_keys)

        # primitive type checking
        if self.schema in (list, set, int, float, str, tuple, chr, bool, dict):
            if isinstance(data, self.schema):
                return data
            else:
                raise SchemaTypeError(self.path, self.schema, data, command=command)

        # dictionary checking
        if issubclass(self.schemaType, dict):
            # schema type is dictionary

            # check data is also a dictionary
            if not isinstance(data, dict):
                raise SchemaTypeError(self.path, self.schema, data, command=command)

            # validated data after comparison to schema
            validData = {}

            x = None

            # matched non-optional schema keys
            coverage = set()

            # loop through data and check against schema
            for k in sorted(data.keys(), key = Schema.priority):
                v = data[k]

                valid = False

                path = self.path + [k]

                if k in self.schema:
                    # fast path, data key matches a schema key
                    sv = self.schema[k]
                    try:
                        # matchValue = Schema(sv, path).validate(
                        #                 v, False, diff_context_retry)
                        matchValue = Schema(sv, path).validate(
                                        v, False, command=command,
                                        warn_unsupported_keys=warn_unsupported_keys)
                    except SchemaMissingKeyError as e:
                        # Collecting Missing keys
                        path_list = []
                        keys_list = e.keys

                        # Remove intersection between e.keys and e.path
                        # e.path is a list of lists of strings
                        for item_path in e.path:
                            for key in item_path[::-1]:
                                if key not in keys_list:
                                    break
                                else:
                                    item_path.remove(key)

                        # Append key to corresponding path
                        path_list += e.path*len(keys_list)
                        for path, missing_keys in zip(path_list,
                                                      keys_list):
                            new_path = path.copy()
                            new_path.append(missing_keys)
                            self.missed.append(new_path)

                        # if the key from data is in the schema, that means it's
                        # covered
                        coverage.add(k)
                    except SchemaError as e:
                        # bad value from user
                        raise
                    else:
                        # found matching key/values
                        coverage.add(k)
                        validData[k] = matchValue
                else:
                    # slow path: data key doesn't match schema key directly
                    for sk in sorted(self.schema.keys(), key = Schema.priority):
                        sv = self.schema[sk]
                        try:
                            # find a schema key that matches the given data
                            # matchKey = Schema(sk, self.path).validate(
                            #             k, False, diff_context_retry)
                            matchKey = Schema(sk, self.path).validate(
                                        k, False, command=command,
                                        warn_unsupported_keys=warn_unsupported_keys)
                        except SchemaMissingKeyError as e:
                            # Collecting Missing keys
                            path_list = []
                            keys_list = e.keys

                            # Remove intersection between e.keys and e.path
                            # e.path is a list of lists of strings
                            for item_path in e.path:
                                for key in item_path[::-1]:
                                    if key not in keys_list:
                                        break
                                    else:
                                        item_path.remove(key)

                            # Append key to corresponding path
                            path_list += e.path*len(keys_list)
                            for path, missing_keys in zip(path_list,
                                                          keys_list):
                                new_path = path.copy()
                                new_path.append(missing_keys)
                                self.missed.append(new_path)
                        except SchemaError:
                            pass
                        else:
                            # found a matching schema key
                            # now test for matching schema value
                            try:
                                # matchValue = Schema(sv, path).validate(
                                #                 v, False, diff_context_retry)
                                matchValue = Schema(sv, path).validate(
                                                v, False, command=command,
                                                warn_unsupported_keys=warn_unsupported_keys)
                            except SchemaMissingKeyError as e:
                                # Collecting Missing keys
                                path_list = []
                                keys_list = e.keys

                                # Remove intersection between e.keys and e.path
                                # e.path is a list of lists of strings
                                for item_path in e.path:
                                    for key in item_path[::-1]:
                                        if key not in keys_list:
                                            break
                                        else:
                                            item_path.remove(key)

                                # Append key to corresponding path
                                path_list += e.path*len(keys_list)
                                for path, missing_keys in zip(path_list,
                                                              keys_list):
                                    new_path = path.copy()
                                    new_path.append(missing_keys)
                                    self.missed.append(new_path)
                                coverage.add(sk)
                            except SchemaError as e:
                                # bad value from user
                                raise
                            else:
                                # found matching key/values
                                coverage.add(sk)
                                validData[matchKey] = matchValue
                                break

            coverage = set(k for k in coverage if not issubclass(type(k), 
                                                                 Optional))

            required = set(k for k in self.schema if not issubclass(type(k), 
                                                                    Optional))

            if self.missed or coverage != required:
                missed_keys = []
                missed_keys_path = []

                # check all keys are there
                if coverage != required:
                    missing = [str(i) for i in required - coverage]
                    missed_keys.extend(missing)
                    for _ in missing:
                        missed_keys_path.append(self.path)

                # Extract path/corresponding_keys from self.missed
                # to raise the SchemaMissingKeyError again.
                for item in self.missed:
                    missed_keys.append(item.pop())
                    missed_keys_path.append(item)
                raise SchemaMissingKeyError(missed_keys_path,
                                            missed_keys, command)

            if len(validData) < len(data):
                # there's stuff in there that's not part of schema
                wrong_keys = set(data.keys()) - set(validData.keys())
                if warn_unsupported_keys:
                    log.warning('Unknown keys {} in path {}. '
                                'Please verify the parser schema.'.format(
                                 wrong_keys, self.path))
                else:
                    raise SchemaUnsupportedKeyError(
                        self.path, wrong_keys, command)

            return validData

        if callable(self.schema):
            try:
                return self.schema(data)
            except Exception as e:
                raise SchemaClassError(self.path, self.schema, data, e) from e

        if self.schema == data:
            return data
        else:
            raise SchemaValueError(self.path, self.schema, data, command)


class Optional(Schema):
    '''Optional Class (Schema)

    Marks an optional part of the schema.
    '''
    pass


class Required(Schema):
    '''Required Class (Schema)

    Marks an required part of the schema.
    '''
    pass


class Any(Optional):
    '''Any Class (Optional, Schema)

    Marks a section of a schema that matches anything. This is effectively a
    wildcard (*).

    Note that Any is also Optional.
    '''

    def __init__(self):
        super().__init__(schema = "*")


class And(Schema):
    '''And Class (Schema)

    Defines a schema of AND relationship, eg, the input data must pass the
    validation of all of the requirements of this Schema.

    Example:
        # requires a string of 'left' or 'right'
        And(str, lambda: s: s in ('left', 'right'))

    Arguments:
        *args : arbitrary args of schema to apply AND to.
    '''

    def __init__(self, *args):
        self.schemas = args

    def __str__(self):
        return "{class_name} {schemas}".format(
            class_name = self.__class__.__name__,
            schemas = self.schemas)

    def validate(self, data, top = False, command='', **kwargs):
        for schema in [Schema(s) for s in self.schemas]:
            data = schema.validate(data, top, command=command, **kwargs)
        return data

class Or(Schema):
    '''Or Class (Schema)

    Defines a schema of OR relationship, eg, the input data must pass the
    validation of one of the requirements of this Schema.

    Example:
        # requires a string or an integer
        Or(str, int)

    Arguments:
        *args : arbitrary args of schema to apply OR to.
    '''

    def __init__(self, *args):
        self.schemas = args

    def __str__(self):
        return "{class_name} {schemas}".format(
            class_name = self.__class__.__name__,
            schemas = self.schemas)

    def validate(self, data, top=False, command='', **kwargs):
        errMsg = []
        for schema in [Schema(s) for s in self.schemas]:
            try:
                return schema.validate(data, top, command=command, **kwargs)
            except:
                errMsg.append("%s does not match %s" % (schema, data))

        raise SchemaError(' and '.join(errMsg))

class Default(Optional):
    '''Default Class (Optional, Schema)

    Defines a schema with a default. Eg, if the schema was not satisfied, the
    default value is added to the input data. A Default schema is also Optional.

    Note:
        using the Default schema changes the input data (due to application of
        default values)

    Usage Criteria:
        if a Default() is part of a dictionary schema type, then keys
        leading to this default value cannot be marked with any other schema
        objects, such as Optional(). Using Default() means that its key-chain
        is automatically mandatory, because regardless of input, the keys
        leading to the default value will always be there.

    Arguments:
        schema (any): input schema requirements
        default (any): default value to apply
    '''

    def __init__(self, schema, default):
        self.default = default
        super().__init__(schema)

    def validate(self, data, top=False, command='', **kwargs):
        if data is None:
            return self.default
        else:
            return super().validate(data, top, command=command, **kwargs)

class Fallback(Optional):
    '''Fallback Class (Optional, Schema)

    Defines a schema with a Fallback. Eg, if the schema was not satisfied, the
    value falls-back to another value in the given data. A Fallback schema
    is also Optional.

    Fallbacks can only be used if the input schema and data to be validated are
    of type dict.

    Note:
        using the Fallback schema changes the input data (due to application of
        fallback values)

    Arguments:
        schema (any): input schema requirements
        fallback (str): string representing the key to fallback to, using '.' as
                        separator to identify dict nesting levels.

    Example:
        # fall back to data['a']['b']['c']
        Fallback(str, 'a.b.c')

    '''

    def __init__(self, schema, fallback):
        self.fallback = tuple(fallback.split('.'))
        super().__init__(schema)

class Use(Schema):

    def validate(self, data, top=False, command='', **kwargs):
        try:
            return self.schema(data)
        except SchemaError as x:
            raise
        except Exception as x:
            f = self.schema.__name__
            raise SchemaError('%s(%r) raised %r' % (f, data, x)) from x


class ListOf(Schema):

    def validate(self, data, top=False, command='', **kwargs):
        if not isinstance(data, list):
            raise SchemaError(self.path, 'list', data)

        valid_list = []
        errors = []
        self.path.append(None)
        for i, item in enumerate(data):
            self.path[-1] = i
            schema = Schema(self.schema, self.path)
            try:
                valid_list.append(schema.validate(item, top, **kwargs))
            except SchemaError as e:
                errors.append(e)
        if errors:
            msg = 'Bad elements in list:\n' + '\n'.join(str(e) for e in errors)
            raise SchemaError(msg)
        return valid_list


class Path(tuple):
    '''Path object (tuple)

    Defines a tuple-like object to be used with ListDict, extending a tuple's
    native ability to compare to also support Any() objects, so that:

        assert Path((1, Any(), 3)) == Path((1, 2, 3))
        assert Path((1, Any(), 3)) == Path((1, 2, 3))

    '''

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        if not isinstance(other, Path):
            return False
        else:
            if len(self) != len(other):
                return False
            else:
                for i,j in zip(self, other):
                    if type(i) is Optional:
                        i = i.schema
                    if type(j) is Optional:
                        j = j.schema

                    # To use regexp i, j have to be string type
                    if type(i) is str and type(j) is str:
                        match = re.compile(i).match(j)
                    else:
                        match = (i == j)
                    if not match:
                        if isinstance(i, Any) or isinstance(j, Any):
                            continue
                        else:
                            return False
                return True

    def is_dynamic(self):
        for obj in self:
            if isinstance(obj, Any):
                return True
        else:
            return False

    def missing_from(self, paths):
        '''missing_from

        Compare the current path to a list of known paths, returning a list
        of matching paths that are missing from the known paths.

        Example:
            Path((1, Any(), 2)).missing_from(((1,2,3), (2,3,4)))
            [(1,2,2)]
        '''

        paths = list(paths)
        
        for path in paths:
            if len(path) != len(self):
                paths.remove(path)
     
        if self.is_dynamic():
            missings = []
            for i, obj in enumerate(self):
                if isinstance(obj, Any):
                    for path in paths:
                        if Path(path[:i+1]) == Path(self[:i+1]):
                            newPath = [j.schema if type(j) is Optional else j 
                                            for j in self]
                            newPath[i] = path[i]
                            missings.extend(Path(newPath).missing_from(paths))
            return list(set(missings))
        else:
            if tuple(self) not in paths:
                return [tuple(self),]

        return []
