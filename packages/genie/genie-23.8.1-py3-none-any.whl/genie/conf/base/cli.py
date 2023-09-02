
__all__ = (
    'CliConfigBuilder',
)

import contextlib
import collections

from .config import CliConfig


class CliConfigBuilder(collections.UserList):
    '''Facilitates Cisco IOS-style CLI configuration string building.

    This object can be handled just like a list of strings but it is highly
    recommended to use only these specific APIs under normal circumstances:

        - append_line
        - append_block
        - submode_context
        - str(self)

    Examples:

        >>> configurations = CliConfigBuilder()
        >>> with configurations.submode_context('my submode'):
        ...     configurations.append_line('my config')
        ... 
        >>> list(configurations)
        ['my submode', ' my config', ' exit']
        >>> str(configurations)
        'my submode\n my config\n exit'
        >>> print(configurations)
        my submode
         my config
         exit

        >>> configurations = CliConfigBuilder(unconfig=True)
        >>> with configurations.submode_context('my submode'):
        ...     configurations.append_line('my config')
        ... 
        >>> list(configurations)
        ['my submode', ' no my config', ' exit']
        >>> str(configurations)
        'my submode\n no my config\n exit'
        >>> print(configurations)
        my submode
         no my config
         exit
    '''
    
    class SubmodeCancelException(Exception):
        '''Internal exception raised with a submode request is cancelled.'''
        pass

    class SubmodeUnconfigException(Exception):
        '''Internal exception raised with a submode must be fully unconfigured.'''
        pass

    unconfig = False
    indent = ' '
    submode_stack = None

    def __init__(self, unconfig=False, device=None):
        '''Initialize a CliConfigBuilder instance.

        Args:
            unconfig: default is False. When True, unconfig mode is turned on
                and, for example, configuration command lines are automatically
                prepended with "no".
        '''
        super().__init__()
        self.unconfig = unconfig
        self.submode_stack = []
        self.device = device

    def append_line(self, item, unconfig_cmd=None, raw=False):
        '''Append a line item to the list of configurations in the current
        submode context.

        If the item is empty (None or empty string), it is ignored and nothing
        is appended.

        If unconfig mode is turned on, the item is prepended with the 'no'
        keyword, unless the unconfig_cmd argument is used.

        Args:
            item: The line item to append.
            unconfig_cmd: When unconfig mode is turned on, use this command instead of the default behavior.
            raw: When True, ignore any processing (such as unconfig mode) and append the item as-is.

        Return:
            None
        '''
            
        if not item:
            # Nothing to configure;
            # Nothing shall be unconfigured either.
            return
        if self.unconfig:
            # Unconfig mode
            if raw:
                # Use item as-is for unconfig too.
                pass
            else:
                if unconfig_cmd is None:
                    # Default unconfig_cmd to the simple 'no' variant
                    unconfig_cmd = 'no ' + item
                item = unconfig_cmd
        if item:
            self.append(item)

    def append_block(self, items, indent=None):
        '''Append a block of line items of configurations in the current submode context.

        If the items argument is an other CliConfigBuilder, each of it's lines are appended.
        If the items argument is a string, it is split on lines and each line is appended.
        Otherwise, an iterable of strings is expected.
        
        Args:
            items: The line items to append. (CliConfigBuilder instance, string
                to be split on lines or an iterable of strings)
            indent: Defaults to None. Specifies an indent string to prepend to
                each line. If True, the default indent (' ') is used.

        Return:
            None
        '''

        if isinstance(items, CliConfigBuilder):
            items = items.data
        elif isinstance(items, CliConfig):
            items = str(items).splitlines()
        elif isinstance(items, str):
            items = items.splitlines()
        if indent:
            if indent is True:
                indent = self.indent
            items = [item and indent + item for item in items]
        self.extend(items)

    @contextlib.contextmanager
    def submode_context(self, submode_cmd, unconfig_cmd=None,
                        cancel_empty=None, exit_cmd='exit'):
        '''Context manager for entering/exiting submodes.

        To be used with Python's "with" statement or a context stack from the
        contextlib module.

        On entering the context, all current configuration lines are put aside
        a new empty list (the new submode's commands) is presented.

        Within the context, any line items appended are handled as per normal.
        The submode_cancel and submode_unconfig methods can be used within the
        context to exit early without processing additional Python commands.

        On exiting the context, the original configuration lines are restored,
        the submode command appended, the new line items appended with an
        appropriate indentation and, finally, the indented exit command is
        appended.

        However, if there are no new configuration items on exiting the
        context, the submode is considered "empty" and the following actions
        are taken instead:

            If "cancel_empty" is True, the submode context is simply
            cancelled/ignored and nothing is appended to the list of
            configurations. The original configuration commands are simply
            restored.

            If "cancel_empty" is False and unconfig mode is NOT on (default
            config mode), the submode_cmd and exit_cmd strings are appended to
            the list of configurations as if it was not empty.

            If "cancel_empty" is False and unconfig mode is on, the "no"
            version of the submode_cmd is used (or unconfig_cmd if specified)
            instead of entering the submode such that the whole submode is
            unconfigured.
            
        Example:

            >>> with configurations.submode_context('my submode'):
            ...     configurations.append_line('my config')

        Args:
            submode_cmd: The command used to enter the submode.
            unconfig_cmd: The command to use if the whole submode needs to be
                unconfigured. See append_line.
            cancel_empty: If True, the submode will be cancelled/ignored
                completely if no sub-configuration commands are appended
                within. If None (the default) it will be cancelled if empty
                only when unconfig mode is on because removing a whole submode
                would unconfigure much more than is configured by simply
                entering it.
            exit_cmd: The command used to exit the submode. Default: 'exit'

        '''
        if cancel_empty is None:
            cancel_empty = self.unconfig
        prev_data = self.data
        self.data = []
        self.submode_stack.append(submode_cmd)
        try:
            yield
        except CliConfigBuilder.SubmodeCancelException:
            self.data = []
            cancel_empty = True
            pass
        except CliConfigBuilder.SubmodeUnconfigException:
            self.data = []
            cancel_empty = False
            pass
        except Exception as e:
            raise
        finally:
            submode_cmd = self.submode_stack.pop()
            sub_data = self.data
            self.data = prev_data
            if sub_data or (not cancel_empty and not self.unconfig):
                if submode_cmd:
                    # submode_cmd
                    #  sub_data...
                    #  exit_cmd
                    self.append_line(submode_cmd, raw=True)
                    self.append_block(sub_data, indent=True)
                    if exit_cmd:
                        self.append_block([exit_cmd], indent=True)
                else:
                    # sub_data...
                    self.append_block(sub_data)
            elif not cancel_empty and self.unconfig:
                # no submode_cmd
                self.append_line(submode_cmd, unconfig_cmd=unconfig_cmd)

    def submode_cancel(self):
        '''Exit submode processing early and cancel the submode if empty.

        To be called from within a submode_cancel scope.

        Example:

            with configurations.submode_cancel('submode1'):
                if some_expression:
                    configurations.submode_cancel()
                # If submode_cancel is called, no submode is entered, the
                # inner cli code below is skipped and execution continues at
                # the outer cli code.
                configurations.append_line('inner cli')
            configurations.append_line('outer cli')
        '''
        if not self.submode_stack:
            raise RuntimeError('submode_cancel called outside a submode context')
        raise CliConfigBuilder.SubmodeCancelException(self.submode_stack[-1])

    def submode_unconfig(self):
        '''Exit submode processing early and unconfig the submode if empty.

        To be called from within a submode_context scope and with unconfig mode turned on.

        Example:

            with configurations.submode_context('submode1'):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()
                # If submode_unconfig is called, no submode is entered, the "no
                # submode1" command is appended, the inner cli code below is
                # skipped and execution continues at the outer cli code.
                configurations.append_line('inner cli')
            configurations.append_line('outer cli')
        '''
        if not self.submode_stack:
            raise RuntimeError('submode_unconfig called outside a submode context')
        if not self.unconfig:
            raise RuntimeError('submode_unconfig called with unconfig mode not turned on')
        raise CliConfigBuilder.SubmodeUnconfigException(self.submode_stack[-1])

    def __repr__(self):
        return "<%s: %r>" % (self.__class__.__name__, self.joinlines())

    def joinlines(self):
        '''Return a string with all configuration lines joined by newline '\\n' characters.'''
        return '\n'.join(self)

    def __str__(self):
        '''Return a string represensation, same as joinlines.'''
        return self.joinlines()

    def splitlines(self):
        '''Return the list of configuration lines, reminiscent of str.splitlines().'''
        return list(self)

# vim: ft=python ts=8 sw=4 et
