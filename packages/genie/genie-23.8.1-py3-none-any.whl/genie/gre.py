import re
import sys

from collections import defaultdict

class bcolours:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class gre(object):
    def __init__(self, *args, **kwargs):
        self.lines = []
        self._current_line = None


    def reset(self):
        self.lines = []
        self._curent_line = None

    def compile(self, *args, **kwargs):
        return gre_pattern(self, *args, **kwargs)

    def __getattr__(self, attr):
        # Not in re, so assume its in compiled object. 
        return getattr(re, attr)

    def colour_output(self):
        text = []
        for match in self.lines:
            # Each time add colour, the line gets longer and span get messed up
            buffer = 0
            seen_span = set()
            if isinstance(match, str):
                if match:
                    line = '{r}{l} {b}<<<<{ec}'.format(r=bcolours.RED,
                                                       l=match, b=bcolours.BLUE,
                                                       ec=bcolours.ENDC)
                else:
                    line = '{r}{l}{ec}'.format(r=bcolours.RED,
                                               l=match,
                                               ec=bcolours.ENDC)
                text.append(line)
                continue
            else:
                line = match.string
                found = match.groupdict()

            colours = defaultdict(lambda: bcolours.RED)
            for i, word in enumerate(match.groups()):
                span = match.span(i+1)
                if not word or span in seen_span:
                    continue
                seen_span.add(span)
                start, end = span
                for i in range(start, end):
                    colours[i] = bcolours.GREEN

            # Draw the colour
            colour = bcolours.RED
            new_line = [colour]
            for i in range(len(line)):
                if colours[i] != colour:
                    colour = colours[i]
                    new_line.append(colour)
                new_line.append(line[i])
            text.append(''.join(new_line))

        # Clear all remaining colours
        text.append(bcolours.ENDC)
        return '\n'.join(text)

    def percentage(self):
        # Check number of word in found, compared to line
        curr_line_lenght = 0
        curr_found_lenght = 0
        for match in self.lines:
            if isinstance(match, str):
                line = match
                found = {}
            else:
                line = match.string
                found = match.groupdict()
            curr_line_lenght += len(line)
            for found_word in found.values():
                if found_word:
                    curr_found_lenght += len(found_word)

        if not curr_line_lenght:
            return 0.0
        return curr_found_lenght / curr_line_lenght

class gre_pattern(object):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.compiled = re.compile(*args, **kwargs)

    def __getattr__(self, attr):
        if attr == 'match':
            def wrapper_match(*args, **kwargs):
                # Ah!
                output = getattr(self.compiled, attr)(*args, **kwargs)
                if output:
                    if self.parent._current_line is not None and self.parent._current_line != args[0]:
                        # It is a new other line and _current hasn't been added
                        self.parent.lines.append(self.parent._current_line)
                        self.parent._current_line = None
                    # Else it is the first time we see this line (None) and it matches
                    # so just add it
                    self.parent.lines.append(output)
                    self.parent._current_line = None
                else:
                    # Line not added, if it isnt added after going through all
                    # the regex choices, then add it
                    if self.parent._current_line is not None and self.parent._current_line != args[0]:
                        # It hasn't been added
                        self.parent.lines.append(self.parent._current_line)
                    self.parent._current_line = args[0]
                return output
            return wrapper_match
        return getattr(self.compiled, attr)


sys.modules['re'] = gre()
