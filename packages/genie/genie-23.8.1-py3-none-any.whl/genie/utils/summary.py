import yaml
import logging
import textwrap

logger = logging.getLogger(__name__)

class Summary(object):
    def __init__(self, title, width):
        # Keep the table look good even though the log level have different
        # lenght
        self.lenght = len('info')
        self.title = title
        self.width = width
        self.summary_msgs = []

        self.title_line = '+{m}+'.format(s='|', m='='*(self.width-2))
        self.subtitle_line = '{s}{m}{s}'.format(s='|', m='='*(self.width-2))
        self.sep_line = '{s}{m}{s}'.format(s='|', m='-'*(self.width-2))
        self.star_line = '{s}{m}{s}'.format(s='|', m='*'*(self.width-2))

        self.add_title_line()
        self.add_message(self.title)
        self.add_title_line()

    def add_title_line(self):
        self.summary_msgs.append(Msg(self.title_line))

    def add_subtitle_line(self):
        self.summary_msgs.append(Msg(self.subtitle_line))

    def add_sep_line(self):
        self.summary_msgs.append(Msg(self.sep_line))

    def add_star_line(self):
        self.summary_msgs.append(Msg(self.star_line))

    def add_message(self, msg, indent=False, level='info'):

        if len(level) > self.lenght:
            # Find longest level so we can make the table looks nice
            self.lenght = len(level)

        if not isinstance(msg, list):
            lines = textwrap.wrap(msg, self.width - 3)
        else:
            lines = []
            for line in msg:
                lines.extend(textwrap.wrap(line, self.width - 3))
        for line in lines:
            self.summary_msgs.append(Msg('| {msg} {l:>{width}}'
                .format(msg=line,
                l='|',
                width=self.width - len(line) - 3), level))

    def print(self):
        for msg in self.summary_msgs:
            if len(msg.level) < self.lenght:
                # Then add the different of white space in front
                msg.msg = ' '*(self.lenght - len(msg.level)) + msg.msg
            getattr(logger, msg.level)(msg.msg)

    def summarize_section(self, message, device=None,
                          level='info', end=True):
        '''Build a summary section as per the provided info'''

        if device:
            self.add_message(msg='* Summary for device: {}'.\
                format(device))
            self.add_sep_line()

        message = self.add_indent(message, end)
        self.add_message(msg=message, level=level)
        self.add_subtitle_line()

    def summarize_profile(self, device, diff=None, golden=False, PTS=True):
        '''Summarize PTS'''
        self.add_message(msg='* Summary for device: {}'.\
            format(device))

        if PTS:
            loc = 'pts_golden_config' if golden else 'Common Setup snapshot'
            loc2 = 'OPS object snapspshot'
        else:
            # Verify configuration
            loc = 'original configuration taken at common setup'
            loc2 = 'the one taken at common cleanup'

        if diff:
            summary_msg = "Comparison between "\
                          "{loc} and {loc2} "\
                          "is different as per the "\
                          "following diffs:\n".format(loc=loc, loc2=loc2)
            message = self.add_indent(summary_msg)
            self.add_message(message, level='error')

            self.add_message(str(diff).splitlines(), level='error')
        else:
            summary_msg = "Comparison between "\
                          "{loc} and OPS object "\
                          "snapshots are equal".format(loc=loc)
            message = self.add_indent(summary_msg)
            self.add_message(message)
        self.add_star_line()


    def add_indent(self, msg, end=True):
        if end:
            return '    - ' + msg
        return '    ' + msg

class TriggerSummary(Summary):

    def summarize_trigger(self, description, info):
        '''Build a summary table for the trigger'''

        description = description.splitlines()
        self.summarize(title="Description", message=description, indent=True)

        title = "Trigger datafile parameters:"
        parameters = yaml.dump(info, default_flow_style=False, indent=4)
        parameters = parameters.splitlines()
        self.summarize(title=title, message=parameters, indent=True)



        #title = "Trigger prerequisities:"
        #summarize(summary=summary, title=title, message=mapper.requirements,
        #    nested=True)
        #title = "Trigger config info:"
        #summarize(summary=summary, title=title, message=mapper.config_info,
        #    nested=True)
        #title = "Trigger verify info:"
        #summarize(summary=summary, title=title, message=mapper._verify_ops_dict,
        #    nested=True)
        #summary.print()
        #log.info("\n")

    def summarize(self, title, message, indent=False):
        '''Build a summary table as per the provided info'''

        self.add_message(msg=title, indent=indent)
        self.add_sep_line()
        self.add_message(msg=message, indent=indent)
        self.add_subtitle_line()


class Msg(object):
    def __init__(self, msg, level='info'):
        self.msg = msg
        self.level = level
