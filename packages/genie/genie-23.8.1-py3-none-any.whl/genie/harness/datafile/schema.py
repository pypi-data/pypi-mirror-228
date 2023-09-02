from pyats.utils.schemaengine import Schema
from pyats.utils.schemaengine import Optional, Any, Use, And, Or, ListOf

def str_to_list(value):
    '''
        Check value type (string) and convert to a list.
    '''

    if isinstance(value, str):
        # convert string to list
        value = [value, ]

    return value

def load_to_objects(value):
    '''load_to_objects

    Load a schema list of [x.y.z, a.b.c] into 'from x.y import z', etc, and
    return the imported z.
    '''
    # convert str to list if
    value = str_to_list(value)

    objs = []

    for name in value:
        try:
            obj = __import__(name.rpartition('.')[0])

            for part in name.split('.')[1:]:
                obj = getattr(obj, part)

            assert callable(obj)
        except (ImportError, AttributeError, AssertionError) as e:
            raise Exception("Cannot translate '%s' into a callable "
                                "object/class" % name) from e
        else:
            objs.append(obj)

    return objs

def devices(value):
    '''Check devices schema'''

    schema = Schema({Any() : str}) # Matching 'uut':None
    try:
        schema.validate(value)
    except:
        # Try to match the other pattern
        schema = Schema({Any() : str}) # Match 'uut': 'None'
        sch={Any(): {# device name
                Optional('iteration'): {
                    Optional('attempt'): int,
                    Optional('interval'): int,
                },
                Any(): Any(),
            }}
        schema = Schema(sch)
    return value

def processors(value):
    '''Check processors schema'''
    sch={Any(): {# processor name
            Optional('pkg'): str,                       # pkg name
            Optional('method'): str,                    # method name
            Optional('parameters'): { Any(): Any() },   # params dictionary
        }}
    schema = Schema(sch)
    return value

def subsections(value):
    '''Check subsections schema'''
    sch={Any(): {# subsection name
            Optional('method'): str,                    # method name
            Optional('parameters'): { Any(): Any() },   # params dictionary
            Optional('processors'): {                   # processors
                Optional('pre'): Use(processors),       # pre processors
                Optional('post'): Use(processors),      # post processors
                Optional('exception'): Use(processors), # exception processors
            },
        }}
    schema = Schema(sch)
    return value

# datafile schema for Genie scripts
mappingdatafile_schema = {
    Optional('devices'): {
        Any(): {                           # devices
            Optional('context'): str,      # context (cli, yang, etc.)
            Optional('pool_size'): int,    # connection pool size
            Optional('netconf_pool_size'): int, # connection pool size for netconf
            Optional('label'): str,        # device label (uut)
            Optional('mapping'): {
                Optional('cli'): Or(str, list),      # cli mapping protocol
                Optional('yang'): str,     # yang mapping protocol
                Optional('netconf'): str,     # yang mapping protocol
                Optional('gnmi'): str,     # yang mapping protocol
                Optional('restconf'): str,     # yang mapping protocol
                Optional('xml'): str,      # xml mapping protocol
                Optional('rest'): str,     # rest mapping protocol
                Optional('web'): str,      # web mapping protocol
                Optional('tgn'): str,      # tgn mapping protocol
                Optional('context'): {     # support for new schema
                    Optional(str):  ListOf # via, alias, pool-size, sleep
                        (
                        {
                       'via': Or(str, list),
                       'alias': str,
                       Optional('pool_size'): int,
                       Optional('sleep'): int
                        }
                    )
                },
                Optional('custom'): {      # custom mapping protocol
                    Any(): Any(),
                },
            },
        },
    },
    Optional('topology'): {                 # topology data mapping
        Optional('links'): {                # links
            Any(): {                        # link names
                Optional('label'): str      # link label
            }
        },
        Any(): {                            # devices
            Optional('interfaces'): {       # interfaces
                Any(): {                    # interface names
                    Optional('label'): str  # interface label
                }
            }
        }
    },
    Optional('parameters'): { Any(): Any() },   # parameters dictionary
    Optional('variables'): { Any(): Any() },    # variables dictionary
}

triggerdatafile_schema = {
    Optional('extends'): Use(str_to_list),  # extends file or list of files
    Optional('uids'): list,
    Optional('groups'): list,
    Optional('data'): Any(),

    Any(): {                                # Trigger Name
        Optional('source'): {
            Optional('pkg'): str,
            Optional('class'): str,
        },
        Optional('timeout'): {
            Optional('max_time'): int,
            Optional('interval'): int,
        },
        Optional('processors'): {           # processors
            Optional('pre'): Use(processors),          # pre processors
            Optional('post'): Use(processors),         # post processors
            Optional('exception'): Use(processors),    # exception processors
        },
        Optional('groups'): list,           # groups
        Optional('count'): int,
        Optional('devices'): list,
        Optional('devices_attributes'): {
            Any(): Any(),
        },
        Optional('verifications'): {
            Any(): {                           # verification name
                Optional('devices'): list,
                Optional('devices_attributes'): Use(devices),
                Optional('iteration'): {
                    Optional('attempt'): int,
                    Optional('interval'): int,
                },
                Optional('parameters'): { Any(): Any() },   # params dictionary
                Optional('exclude'):list,
            },
        },
        Optional('tgn_timeout'): int,          # tgn timeout
        Optional('tgn_delay'): int,            # tgn delay
        Optional('tgn_max_outage'): Or(int, float),       # tgn max acceptable outage
        Optional('genie_telemetry'): bool,          # enable/disable telemetry
        Optional('telemetry_plugins'): list,        # telemetry plugins
        Optional('skip_global_verifications'): list,        # Skip global verification
        Any(): Any(),                       # any data for Triggers
        Optional('sections'): {
            Any(): {
                Optional('parameters'): {                   # section parameters
                    Any(): Any(),                           # any data for parameters
                },
                Optional('processors'): {                   # processors
                     Optional('pre'): Use(processors),       # pre processors
                     Optional('post'): Use(processors),      # post processors
                     Optional('exception'): Use(processors), # exception processors
                },
            }
        },
    },
    Optional('global_processors'): {        # Global processors
        Optional('pre'): Use(processors),          # pre processors
        Optional('post'): Use(processors),         # post processors
        Optional('exception'): Use(processors),    # exception processors
    },
    Optional('order'): list,
    Optional('parameters'): { Any(): Any() },   # parameters dictionary
    Optional('variables'): { Any(): Any() },    # variables dictionary
}

verificationdatafile_schema = {
    Optional('extends'): Use(str_to_list),  # extends file or list of files
    Optional('uids'): list,
    Optional('groups'): list,

    Any(): {                                # Verification Name
        Optional('source'): {
            Optional('pkg'): str,
            Optional('class'): str,
        },
        Optional('processors'): {           # processors
            Optional('pre'): Use(processors),          # pre processors
            Optional('post'): Use(processors),         # post processors
            Optional('exception'): Use(processors),    # exception processors
        },
        Optional('groups'): list,           # groups
        Optional('count'): int,
        Optional('exclude'):list,
        Optional('iteration'): {
            Optional('attempt'): int,
            Optional('interval'): int,
        },
        Optional('parameters'): { Any(): Any() },   # params dictionary
        Optional('devices'): list,
        Optional('devices_attributes'): Use(devices),
        Optional('genie_telemetry'): bool,          # enable/disable telemetry
        Optional('telemetry_plugins'): list,        # telemetry plugins
        Any(): Any(),                       # any data for Verifications
    },
    Optional('global_processors'): {        # Global processors
        Optional('pre'): Use(processors),          # pre processors
        Optional('post'): Use(processors),         # post processors
        Optional('exception'): Use(processors),    # exception processors
    },
    Optional('parameters'): { Any(): Any() },   # parameters dictionary
    Optional('variables'): { Any(): Any() },    # variables dictionary
}

configdatafile_schema = {
    Optional('devices'): {
        Any(): {                                    # devices
            Any(): {                                # configuration order
                Optional('type'): str,              # (setup|cleanup) - Refer to common setup and cleanup
                Optional('config'): str,            # config path
                Optional('sleep'): int,             # sleep time between applying cfg
                Optional('invalid'): list,          # expected invalid cfgs
                Optional('jinja2_config'): str,     # jinja2 file
                Optional('vrf'): str,               # vrf for copying
                Optional('jinja2_arguments'): {     # jinja2 arguments
                    Any(): Any()                    # key and data
                },
                Optional('configure_arguments'): dict, # unicon configure service arguments
                Optional('verify'): {
                    'method': str,                  # Method to call for timeout
                    'max_time': int,                # max_time
                    'interval': int,                # interval
                    Any(): Any(),                   # extra parameters
                },
            },
        },
    },
    Optional('exclude_config_check'): Any(),
    Optional('sleep'): Any(),
    Optional('parameters'): { Any(): Any() },   # parameters dictionary
    Optional('variables'): { Any(): Any() },    # variables dictionary
}

ptsdatafile_schema = {
    Optional('extends'): Use(str_to_list),  # extends file or list of files

    Any(): {                                # Feature Name
        Optional('source'): {
            Optional('pkg'): str,
            Optional('class'): str,
        },
        Optional('exclude'):list,
        Optional('devices'): list,
        Optional('devices_attributes'): Use(devices),
    },
    Optional('parameters'): { Any(): Any() },   # parameters dictionary
    Optional('variables'): { Any(): Any() },    # variables dictionary
}

subsectiondatafile_schema = {
    Optional('extends'): Use(str_to_list),  # extends file or list of files
    Optional('parameters'): { Any(): Any() },   # parameters dictionary
    Optional('variables'): { Any(): Any() },    # variables dictionary

    Optional('setup'): {                            # common setup
        Optional('sections'): Use(subsections),     # extends subsections
        Optional('order'): list,                    # exclusion list
        Optional('processors'): {                   # processors
            Optional('pre'): Use(processors),       # pre processors
            Optional('post'): Use(processors),      # post processors
            Optional('exception'): Use(processors), # exception processors
        },
        Optional('telemetry_plugins'): list,        # telemetry plugins
    },

    Optional('cleanup'): {                          # common cleanup
        Optional('sections'): Use(subsections),     # extends subsections
        Optional('order'): list,                    # exclusion list
        Optional('processors'): {                   # processors
            Optional('pre'): Use(processors),       # pre processors
            Optional('post'): Use(processors),      # post processors
            Optional('exception'): Use(processors), # exception processors
        },
        Optional('telemetry_plugins'): list,        # telemetry plugins
    },
}
