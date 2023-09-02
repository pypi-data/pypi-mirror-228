import json
from collections import namedtuple, deque, namedtuple


class Config(object):
    '''Class to store show-running output

    Allows to visualize it like a dictionary

    Args:
        output (`str`): show-running output

    Returns:
            Config object

    Examples:

        >>> output = Config(device.execute('show-running'))
        >>> output.tree()
    '''

    def __init__(self, output, exclude=None):
        # Show running output
        self.output = output

        # Exclude line from show running
        self.exclude = ['!', None, '\r', '']
        if exclude:
            self.exclude.extend(exclude)

    def tree(self):
        # If we can load it through json, then its already a good format
        try:
            self.config = json.loads(self.output)
        except Exception:
            # Nope!
            pass
        else:
            return
        # Go through each line
        Level = namedtuple('Level', ['indentation', 'data'])
        # Holds configuration
        self.config = {}

        # Stack of indendation seen so far
        _previous = deque()
        _previous.append(Level(0, self.config))
        # Current indendation
        _curr = self.config
        # holds the data of the new information. In case we need to go to next
        # level, it holds it
        _future = self.config

        for line in self.output.split('\n'):
            # Disregard line we do not care about
            line_strip = line.strip()
            if line_strip in self.exclude or line_strip.startswith('!'):
                # Ignore those lines
                continue

            # Remove from '\r' from line
            line = line.replace('\r', '')

            # Replace control-C to '^C'
            line = line.replace('\x03', '^C')

            # Alright line we care about

            # Calculate curr_indentation
            curr_indentation = len(line) - len(line.lstrip())

            # Remove indendation of the line
            line = line.strip()

            if _previous is None or\
               _previous[-1].indentation == curr_indentation:
                # Same level, so same parent

                _future = _curr[line] = {}
            elif _previous[-1].indentation < curr_indentation:
                # New level!

                _curr = _future
                _future = _curr[line] = {}
                _previous.append(Level(curr_indentation, _curr))

            elif _previous[-1].indentation > curr_indentation:
                # Going back to previous level
                # Though, it could be, many level, or some

                # The goal is to find what indentation we are at, which
                # will tell us the parent
                for i in range(len(_previous)):
                    item = _previous[-1]
                    if item.indentation == curr_indentation:
                        _curr = item.data
                        _future = _curr[line] = {}
                        break
                    else:
                        if len(_previous) == 1:
                            # This is the last level and it still wasnt this
                            # one! This is a corner case. Instead of crashing
                            # we go back to the first level.
                            # Seen this case in MOTD
                            _curr = item.data
                            _future = _curr[line] = {}
                            break
                        _previous.pop()
                else:
                    raise Exception("Couldn't find indentation '{i} for "
                                    "'{line}'".format(i=curr_indentation,
                                                      line=line))
