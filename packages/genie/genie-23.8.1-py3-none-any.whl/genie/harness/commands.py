import json
import logging
import pathlib
import traceback

from pyats.topology import loader
from pyats.cli.base import Subcommand
from genie.harness.datafile.loader import ConfigdatafileLoader

logger = logging.getLogger(__name__)


class ValidateJinja2ConfigFile(Subcommand):
    '''
    Validates the provided genie config file for jinja2 rendering.
    '''

    name = 'jinja2_config'
    help = 'validate genie config file jinja2 rendering'

    usage = '{prog} [file] [options]'

    description = '''
Validates the provided genie config file for jinja2 rendering.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # add testbed file
        self.parser.add_argument('config_file',
                                 metavar = '[file]',
                                 type = str,
                                 help = 'Genie config datafile to validate')

        # check connections
        self.parser.add_argument('--testbed-file',
                                 dest = 'testbed',
                                 type = loader.load,
                                 required = True,
                                 help = "Testbed file (required)")

        self.parser.add_argument('--devices',
                                 type = str,
                                 nargs = '+',
                                 help = 'Devices to render configs for (optional)')

        self.parser.add_argument('--sequence',
                                 type = str,
                                 nargs = '+',
                                 help = 'Sequence(s) to render (optional)')

    def run(self, args):
        testbed = args.testbed

        config_data = ConfigdatafileLoader(testbed=testbed, enable_extensions=True).load(args.config_file)

        device_config_text = {}
        for dev, device_config_data in config_data['devices'].items():
            if args.devices:
                if dev not in args.devices:
                    continue
            device_config_text[dev] = {}
            device = testbed.devices[dev]
            sequence = device_config_data.keys()
            for seq in sorted(sequence, key=int):
                if args.sequence:
                    if str(seq) not in args.sequence:
                        continue
                conf = device_config_data.get(seq)
                if conf.get('jinja2_config'):
                    fullpath = pathlib.Path(conf.get('jinja2_config'))
                    path = str(fullpath.absolute().parent)
                    file = fullpath.name
                    jinja2_arguments = conf.get('jinja2_arguments', {})
                    try:
                        rendered = device.api.load_jinja_template(
                            path = path,
                            file = file,
                            **jinja2_arguments
                        )
                    except Exception:
                        device_config_text[dev][seq] = f"Error: {traceback.format_exc()}"
                    else:
                        device_config_text[dev][seq] = rendered

        for dev, seq_data in device_config_text.items():
            for seq in seq_data:
                text = seq_data[seq]
                if 'Error:' in text:
                    text = '\n'.join(text.splitlines()[-3:])
                print(f'\nDevice {dev} sequence {seq}:\n{text}')
