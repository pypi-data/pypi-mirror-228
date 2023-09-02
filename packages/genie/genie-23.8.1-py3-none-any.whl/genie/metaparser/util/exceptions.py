# import logging
from logging import Logger

log = Logger(__name__)

'''
    Errors related to utils module
'''

class SchemaError(Exception):

    """Error during Schema validation."""

    def joinPath(self, path):
        if path:
            return '.'.join([str(i) for i in path])
        else:
            return None

class SchemaMissingKeyError(SchemaError):
    def __init__(self, path, keys, command=''):
        self.path = path
        self.keys = keys
        self.missing_list = []
        super().__init__(self.format(path, keys, command))

    def format(self, path, keys, command=''):
        new_list = []
        msg = []
        if command:
            msg.append("Show Command: {command}".format(command=command))
        if not path:
            for item in keys:
                if item not in new_list:
                    new_list.append(item)
            msg.append("Missing keys: %s" % (new_list))
        else:
            new_list = []
            for item, value in zip(path, keys):
                tmp_item = item.copy()
                if value not in item:
                    tmp_item.append(value)
                new_list.append(tmp_item)
            msg.append("Missing keys: %s" % (new_list))

        self.missing_list = new_list
        return '\n'.join(msg)


class SchemaTypeError(SchemaError):
    def __init__(self, path, schema, data, detail=None, command=''):
        self.path = path
        self.data = data
        self.type = schema
        super().__init__(
            self.format(self.joinPath(path), schema, data, detail, command))

    def format(self, path, schema, data, detail, command=''):
        msg = []
        if command:
            msg.append("Show Command: {command}".format(command=command))
        if not path:
            msg.append("Expected type '%s' but got type '%s'(%s)" %
                       (str(schema), data, type(data)))
        else:
            msg.append("%s: Expected type '%s' but got type '%s'(%s)" %
                       (path, str(schema), data, type(data)))

        if detail:
            msg.append("Details: '%s'" % detail)

        return '\n'.join(msg)


class SchemaValueError(SchemaError):
    def __init__(self, path, schema, data, detail=None, command=''):
        super().__init__(
            self.format(self.joinPath(path), schema, data, detail, command))

    def format(self, path, schema, data, detail=None, command=''):
        msg = []
        if command:
            msg.append("Show Command: {command}".format(command=command))
        if not path:
            msg.append("Expected '%s' but got '%s'" % (str(schema), str(data)))
        else:
            msg.append("%s: Expected '%s' but got '%s'" %
                       (path, str(schema), str(data)))

        if detail:
            msg.append("Details: '%s'" % detail)

        return '\n'.join(msg)


class SchemaUnsupportedKeyError(SchemaError):
    def __init__(self, path, keys, command=''):
        self.path = path
        self.keys = keys
        self.unsupported_keys = []
        super().__init__(self.format(self.joinPath(path), keys, command))

    def format(self, path, keys, command=''):
        new_list = []
        msg = []
        if command:
            msg.append("Show Command: {command}".format(command=command))
        if not path:
            for item in keys:
                if item not in new_list:
                    new_list.append(item)
            msg.append("Unsupported keys: %s" % [str(i) for i in keys])
        else:
            for key in keys:
                # copy the path and append the key to the end to get the full path,
                # then append to the list of unsupported key paths
                tmp_path = self.path.copy()
                if key not in tmp_path:
                    tmp_path.append(key)
                new_list.append(tmp_path)

            msg.append("%s: Unsupported keys: %s" %
                       (path, [str(i) for i in keys]))

        self.unsupported_keys = new_list
        return '\n'.join(msg)


class SchemaClassError(SchemaError):
    def __init__(self, path, cls, data, detail=None, command=''):
        super().__init__(
            self.format(self.joinPath(path), cls, data, detail, command))

    def format(self, path, cls, data, detail, command=''):
        msg = []
        if command:
            msg.append("Show Command: {command}".format(command=command))
        if not path:
            msg.append("Could not instantiate class '%s' with '%s'" %
                       (cls, data))
        else:
            msg.append("%s: Could not instantiate class '%s' with '%s'" %
                       (path, cls.__name__, data))

        if detail:
            msg.append("Details: '%s'" % detail)

        return '\n'.join(msg)


class SchemaFallbackError(SchemaError):
    def __init__(self, path, data, command=''):
        super().__init__(self.format(self.joinPath(path), data, command))

    def format(self, path, data, command=''):
        msg = []
        if command:
            msg.append("Show Command: {command}".format(command=command))
        msg.append('%s not found in %s' % (path, data))
        return '\n'.join(msg)


class SchemaFallbackLoopError(SchemaError):
    def __init__(self, a, b, command=''):
        super().__init__(
            self.format(self.joinPath(a), self.joinPath(b), command))

    def format(self, a, b, command=''):
        msg = []
        if command:
            msg.append("Show Command: {command}".format(command=command))
        if a == b:
            msg.append("cannot fallback to self: '%s'" % (a, ))
            return '\n'.join(msg)
        else:
            msg.append("Detected infinite fallback loop: '%s' <---> '%s'" %
                       (a, b))
            return '\n'.join(msg)


class SchemaFallbackCall(SchemaError):
    def __init__(self, path, diff_context_retry, command=''):
        self.path = path
        super().__init__(path)
        msg = []
        if command:
            msg.append("Show Command: {command}".format(command=command))
        msg.append('%s parser fallback type has been used' %
                   (diff_context_retry))
        log.info('\n'.join(msg))


class SchemaEmptyParserError(Exception):
    def __init__(self, data, command=''):
        msg = []
        if command:
            msg.append("Show Command: {command}".format(command=command))
        msg.append("Parser Output is empty")
        super().__init__('\n'.join(msg))

class ParseSelectedKeysException(Exception):
    def __init__(self):
        pass

class InvalidCommandError(Exception):

    """Error during invalid command execution"""

    def __init__(self, command=''):
        msg = []
        if command:
            msg.append("Show Command: {command}".format(command=command))
        msg.append("Invalid command has been executed")
        super().__init__('\n'.join(msg))
