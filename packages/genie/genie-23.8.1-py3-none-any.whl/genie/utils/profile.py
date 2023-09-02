# Python
import os
import sys
import dill
import json
import logging
import jsonpickle
import prettytable
import yaml

# ATS
# import pcall
import importlib
try:
    pcall = importlib.import_module('pyats.async').pcall
except ImportError:
    from pyats.async_ import pcall
# # import pcall
# from pyats.async import pcall
from pyats.easypy import runtime
from pyats.log.utils import banner
from pyats.datastructures import AttrDict
from pyats.aetest.exceptions import DatafileError

# Genie
from genie.abstract import Lookup
from genie.utils.diff import Diff
from genie.libs.sdk import genie_yamls
from genie.ops.utils import get_ops_exclude
from genie.utils.summary import Summary
from genie.harness.utils import load_class
from genie.libs.parser.utils import get_parser_exclude
from genie.harness.utils import recursive_trim
from genie.harness.datafile.loader import PtsdatafileLoader
from genie.harness.exceptions import GenieTgnError

# Module variables
log = logging.getLogger(__name__)


class Profile(object):

    @classmethod
    def compare(cls, compare1, compare2, pts_data=None, testbed=None, verf_data=None):

        # Check if provided comapre is a an unpickled file
        if not isinstance(compare1, dict):
            # Then assume its a pickle
            compare1 = unpickle(compare1)

        if not isinstance(compare2, dict):
            # Then assume its a pickle
            compare2 = unpickle(compare2)

        # Collect features to be compared
        features = set(compare1).intersection(set(compare2))

        summarized_dict = {}

        # Collect the rest of the features to include them later in the summary
        features_diffs = set(compare1) - set(compare2)
        features_diffs = features_diffs.union(set(compare2) - set(compare1))

        summarized_dict.setdefault('not_compared', features_diffs)

        if not pts_data:
            pts_data = load_datafile(genie_yamls.pts_datafile,
                PtsdatafileLoader)
        elif not isinstance(pts_data, dict) and os.path.isfile(pts_data):
            pts_data = load_datafile(pts_data, PtsdatafileLoader)

        for feature in features:

            failed = []
            passed = []
            for device in sorted(compare2[feature]):
                exclude = ['device', 'maker', 'diff_ignore', 'callables',
                           '(Current configuration.*)', 'ops_schema']


                # Find the parser class
                dev = testbed.devices[device]
                try:
                    exclude.extend(get_ops_exclude(feature, dev))
                except Exception:
                    try:
                        exclude.extend(get_parser_exclude(feature, dev))
                    except Exception:
                        pass

                # Add from pts datafile
                try:
                    exclude.extend(pts_data[feature]['exclude'])
                except KeyError:
                    # If not in PTS datafile, then use the verification datafile
                    pass

                # Add the global excludes too
                try:
                    exclude.extend(pts_data['exclude'])
                except KeyError:
                    pass

                diff = Diff(compare1[feature][device],
                            compare2[feature][device],
                            exclude=exclude)
                diff.findDiff()

                if len(diff.diffs):
                    failed.append((device, diff))
                    log.info("Verify '{f}' snapshot with initial snapshot "
                        "for device '{d}'\n    Failed"
                        .format(f=feature, d=device))
                else:
                    passed.append(device)

            if feature not in summarized_dict:
                summarized_dict.setdefault(feature, {})
                summarized_dict[feature].setdefault('failed', {})
                summarized_dict[feature].setdefault('passed', {})

            for device, diff in failed:
                summarized_dict[feature]['failed'][device] = diff

            for device in passed:
                # Include the rest of the devices, not failed, in the
                # summary table
                summarized_dict[feature]['passed'][device] = {}

            log.info("\n")

        return summarized_dict


    @classmethod
    def learn_features(cls, features, testbed, pts_data=None, current_instance=None,
                       testscript=None, file=None, location=None, pts_name=None):

        if not features:
            raise KeyError("No features were passed to be learnt")

        asynchronous_profile_output = {}

        # create results dictionary to be passed to pcall
        learnt_dict = {}

        if not pts_data:
            pts_data = load_datafile(genie_yamls.pts_datafile,
                PtsdatafileLoader)
        elif not isinstance(pts_data, dict) and os.path.isfile(pts_data):
            pts_data = load_datafile(pts_data, PtsdatafileLoader)

        for feature in features:

            # Get parsed data from the pts datafile
            try:
                new_pts_data = pts_data[feature]
            except KeyError:
                raise KeyError("'{f}' does not exists in pts_data "
                    "file".format(f=feature))

            # Could device or alias be passed, so check
            try:
                # This will search for device name and alias
                devices = [testbed.devices[dev]\
                           for dev in new_pts_data['devices']]
            except KeyError:
                # this mean,there was no new_pts_data['device']
                # So just uses uut device
                devices = testbed.find_devices(aliases=['uut'])

                # Make sure its only one
                if len(devices) < 1:
                    # No devices was found, unlikely as uut was set in init
                    raise Exception("No 'uut' device was found")
                elif len(devices) > 1:
                    # More than 1 device was found with uut
                    raise Exception("More than one device were found "\
                        "with alias 'uut'; {d}".format(d=devices))

            # Add feature to the created dictionary to be passed to pcall
            learnt_dict.setdefault(feature, {})

            # Remove dup
            seen = set()
            seen_add = seen.add
            devices = [x for x in devices if not (x in seen or seen_add(x))]
            devices_names = [x.alias if hasattr(x, 'alias') else x.name for x in devices]

            # Use single target pcall functionality to profile the devices
            # in parallel
            log.info("Profile '{f}' on '{d}'".format(f=feature, d=devices_names))

            try:
                asynchronous_profile_output[feature] = pcall(asynchronous_profile,
                    ckwargs={'feature':feature, 'pts_data':new_pts_data,\
                    'learnt_dict':learnt_dict},
                    device = tuple(devices))
            except Exception as e:
                raise Exception("Failed in learning '{f}' feature\n{e}".format(
                    f=feature, e=e)) from None

            # Stored the PTS in this structure
            # {feature:{dev:object, dev2:object2},
            #  feature2:{dev:object, dev2:object2}}
            for item in asynchronous_profile_output[feature]:
                feature_obj = item['obj']
                for device, value in sorted(item.items()):
                    # item = 
                    # {'device1': 'pickled string',
                    #  'device2': 'pickled string2',
                    #  'obj': <Feature object to use for unpickle later>}
                    if device == 'obj':
                        continue

                    # unpickle the learnt_pts string to proceed with the comparison
                    if hasattr(feature_obj, 'unpickle'):
                        obj = feature_obj.unpickle(value)
                    else:
                        obj = dill.loads(value)

                    # To be used later when saving the pts objects saved. Save with 
                    # device name or alias
                    # if device in devices_names and hasattr(devices[device], 'alias')
                    if hasattr(testbed.devices[device], 'alias'):
                        device_nickname = testbed.devices[device].alias
                    else:
                        device_nickname = testbed.devices[device].name

                    learnt_dict[feature][device_nickname] = obj

        # Pickle the PTS learnt in CommonSetup to be used later as a
        # golden PTS file
        if not file:
            if testscript:
                testscript.parameters['learnt_dict'].update(learnt_dict)
                if set(testscript.parameters['learnt_dict'].keys()) == set(testscript.pts_features):
                    # Only pickle 'learnt_dict' when all the commonSetup features
                    # got learnt
                    pickled_file = pickle(testscript.parameters['learnt_dict'], location=location,
                        pts_name=pts_name)
            else:
                # Covering the case when running as standalone and user wants
                # the pickled pts to use later
                pickled_file = pickle(learnt_dict, location=location,
                    pts_name=pts_name)

        return learnt_dict


def load_datafile(datafile, cls):

    loader_cls = cls
    try:
        loader = loader_cls()
        data = loader.load(datafile)
    except Exception as e:
        raise DatafileError("Failed to load the datafile '%s'"
                            % datafile) from e
    return data

def asynchronous_profile(device, feature, pts_data, learnt_dict):
    '''Use asynchronous execution when profiling features on devices'''

    # Use alias in the banners
    log.info(banner("Profile '{f}' on '{d}'".format(f=feature,
        d=device.alias)))

    # Is it a show command or a feature?
    # All features should be a single word and not start with show
    # Hope that rule is strong enough...
    if not feature.startswith('show') and len(feature.split()) == 1:
        # Load the class, use abstraction if needed
        # otherwise just load the class
        try:
            lib = load_class(pts_data, device)
            # Right now supports ops,  but if any other class
            # can be instantiated like this it would work
            lib = lib(device)
            lib.learn()
        except Exception as e:
            raise Exception("Issue with loading a pts class"
                " or when learning the '{f}' feature on device '{d}'\n{e}".format(
                f=feature, d=device.name, e=e)) from None
        # Pickle the learnt object to be sent back to the pcall call
        try:
            pickled_string = lib.pickle(lib)
        except Exception:
            raise Exception("Issue while pickling the object '{lib}'".\
                format(lib=lib))
    else:
        # A show command
        try:
            output = device.parse(feature)
        except Exception as e:
            raise Exception("Issue with '{f}'\n{e}".format(f=feature, e=e)) from None
        pickled_string = dill.dumps(output)
        lib = feature

    # Keep track of those via alias, so different testbed with same
    # alias can work
    if device.alias:
        learnt_dict[feature][device.alias] = pickled_string
    else:
        learnt_dict[feature][device.name] = pickled_string

    # Send the object back to use it for unpickling
    learnt_dict[feature]['obj'] = lib

    return learnt_dict[feature]

def unpickle(file):
    '''Unpickle file; Used for Golden profile'''
    if not file:
        raise Exception('No Golden PTS profile file provided')

    with open(file, 'rb') as f:
        return dill.load(f)

def pickle(pts, location=None, pts_name=None):
    '''Pickle file; Used for Golden profile'''

    if not pts:
        return

    # location of the pts file (default to runtime dir)
    location = location or runtime.directory

    # differentiate between pts saved during CS and the standalone one
    # (ex:trigger)
    pts_name = pts_name or 'pts'

    # primary pickle file (default to runtime dir)
    file = os.path.join(location, pts_name)

    # Save the file to be used later as golden
    with open(file, 'wb') as f:
        # Create the pickle object
        dill.dump(pts, f)

    # Create human readable json files
    for feature in pts:
        for dev, ops in pts[feature].items():
            # human readable json pts
            file = os.path.join(location, '{l}_{d}_{f}_pts.json'.\
                format(l=pts_name, f=feature, d=dev))

            with open(file, 'w') as f:
                dump_data = {feature:{dev:ops}}
                json.dump(recursive_trim(
                    json.loads(jsonpickle.dumps(dump_data)),
                        keys = ['py/object', '__dict__']), f, indent = 4)

    return file

def summarize_comparison(summarized_dict, passed_feature=None,
    print_not_compared=True):
    '''Summarize the features comparison'''

    for feature in summarized_dict:
        if passed_feature and passed_feature != feature:
            continue

        if feature == 'not_compared':
            continue

        # Create Summary
        summary = Summary(title='{f} PTS Summary'.format(f=feature.title()),
            width=150)

        for device in summarized_dict[feature]['failed']:
            summary.summarize_profile(
                diff=summarized_dict[feature]['failed'][device],
                device=device)

        for device in summarized_dict[feature]['passed']:
            summary.summarize_profile(device=device)

        summary.print()

    if summarized_dict['not_compared'] and print_not_compared:
        for feature in summarized_dict['not_compared']:
            # Create Summary
            summary = Summary(title='{f} PTS Summary'.format(f=feature.title()),
                width=150)
            message=("No comparison performed, it wasn't learnt at this "
                "section".format(f=feature))
            summary.summarize_section(message=message)
            summary.print()

#--------------------------- TRAFFIC PROFILING ---------------------------------

def pickle_traffic(tgn_profile, location=None, tgn_profile_name=None):
    '''Dump traffic profile to runtime directory'''

    # If no traffic profile or not a prettytable object, do nothing
    if not tgn_profile or not isinstance(tgn_profile, prettytable.PrettyTable):
        return

    log.info(banner("Save traffic profile to Genie Logs"))

    # location of the traffic_profile file (default to runtime dir)
    location = location or runtime.directory

    # differentiate between pts saved during CS or within trigger/standalone
    tgn_profile_name = tgn_profile_name or 'traffic_profile'

    # filename
    tgn_file = os.path.join(location, tgn_profile_name)

    # Copy file to location
    with open(tgn_file, 'w') as file:
        file.write(tgn_profile.get_string())

    return tgn_file

def unpickle_traffic(file):
    '''Unpacks traffic profile and returns a prettytable object'''

    # Check if running from regression with different branches
    if not os.path.isfile(file):
        if 'BRANCH' not in os.environ:
            raise GenieTgnError("Golden traffic profile is a directory, branch "
                            "information not provided")
        file = os.path.join(file,
                '{br}/golden_traffic_profile'.format(br=os.environ['BRANCH']))

    if not os.path.exists(file) or not os.path.isfile(file):
        raise GenieTgnError('Golden traffic profile file not found')

    # Init
    golden_profile = prettytable.PrettyTable()
    # ['Source/Dest Port Pair', 'Traffic Item', 'Tx Frames', 'Rx Frames', 'Frames Delta', 'Tx Frame Rate', 'Rx Frame Rate', 'Loss %', 'Outage (seconds)']
    golden_profile.field_names = ['Source/Dest Port Pair', 'Traffic Item',
                                  'Tx Frames', 'Rx Frames', 'Frames Delta',
                                  'Tx Frame Rate', 'Rx Frame Rate', 'Loss %',
                                  'Outage (seconds)']

    # Read data and create prettytable profile
    with open(file, 'r') as f:
        for line in f.read().splitlines():
            if '--------' in line or 'Outage (seconds)' in line:
                continue
            row_values = []
            for item in line.strip().split('|'):
                if item:
                    row_values.append(item.strip())
            golden_profile.add_row(row_values)

    # Align data
    golden_profile.align = "l"

    return golden_profile

def unpickle_stream_data(file, copy=False, copy_file=None):
    '''Unpacks file containing traffic stream data values
       Returns a python dictionary containing the data
       Copies user provided file to runtime logs if requested
       '''

    # Check file exists
    if not os.path.exists(file) or not os.path.isfile(file):
        raise GenieTgnError('Traffic stream data file not found')

    log.info(banner("Reading traffic streams data file"))

    # Streams dict
    with open(file) as f:
        streams_dict = yaml.safe_load(f)

    # Copy user provided ixia.yaml to runtime logs
    if copy and copy_file:
        streams_file = os.path.join(runtime.directory, copy_file)
        # Copy file to runtime logs
        with open('{}.yaml'.format(streams_file), 'w') as f:
            yaml.dump(streams_dict, f, default_flow_style=False)

    # Return dcit
    return streams_dict

