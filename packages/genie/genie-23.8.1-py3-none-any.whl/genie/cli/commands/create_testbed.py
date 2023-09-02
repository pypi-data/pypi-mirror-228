from pyats.cli.base import Subcommand
from pkg_resources import iter_entry_points

TOPOLOGY_LOADER_GROUP = "pyats.topology.loader"

class CreateTestbed(Subcommand):
    name = 'testbed'
    help = 'create a testbed file automatically'
    
    usage = '{prog} [source] [arguments]'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parser.add_argument('source',
                                metavar='[source]',
                                type=str,
                                help="Source of where to retrieve device data.")

        self.parser.add_argument('--output',
                    action='store',
                    type=str,
                    help='File location to output the created testbed yaml.',
                    required=True)
    
    def run(self, args):
        sources = []
        # Load entry point from pyats.topology.loader
        for entry in iter_entry_points(group=TOPOLOGY_LOADER_GROUP):
            sources.append(entry.name)
            if entry.name == args.source:
                creator = entry.load()
                instance = creator()
                instance.to_testbed_file(args.output)
                instance.print_result()
                return
        else:
            suggestions = ''
            if len(sources) > 0:
                suggestions = '\n\nvalid options:\n' + '\n'.join(
                                            '- ' + source for source in sources)
            # If entry point is not found
            raise Exception('please make sure pyats.contrib is installed. ' +
                            "If not, please do 'pip install pyats.contrib'.\n" +
                            "\ninvalid option: %s%s" %
                                                     (args.source, suggestions))

            
