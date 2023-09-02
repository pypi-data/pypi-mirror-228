'''
Processors for Genie Triggers
'''

# Python
import time
import logging
import requests
import warnings
import functools

# ATS
from pyats.aetest import Testcase, skip
from pyats.log.utils import banner
from pyats.log import managed_handlers
from pyats.log.warnings import enable_deprecation_warnings
from pyats.results import TestResult, Passed, Failed, Skipped, Passx, Aborted, Errored
from pyats.aetest.base import TestableId
from pyats.aetest.sections import SetupSection
from pyats.datastructures import AttrDict
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure

# Genie
from genie.libs import sdk
from genie.abstract import Lookup
from genie.harness.utils import connect_device
from genie.harness.exceptions import GenieTgnError
from genie.utils.profile import pickle_traffic, unpickle_traffic, unpickle_stream_data

# Logger
log = logging.getLogger(__name__)

enable_deprecation_warnings(__name__)

DEPRECATION_MSG = \
    "This processor moved to genie.libs.sdk.abstracted_libs.processors. "\
    "Please update pkg/method in datafiles. This processor will be depreciated"\
    " in near future."

def report(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        finally:
            try:
                func.result = wrapper.result
            except AttributeError:
                # Default is already passed
                pass
        return result
    return wrapper

### MOVED
def _get_connection_class(section):

    conn_class_name = None
    for dev in section.parameters['testbed'].find_devices(type='tgn'):
        for con in dev.connections:
            try:
                conn_class_name = dev.connections[con]['class'].__name__
            except:
                continue
    return conn_class_name

# ==============================================================================
# processor: clear_traffic_statistics
# ==============================================================================
### MOVED
def disable_clear_traffic(section, clear_stats_time=10):

    log.info("Processor 'clear_traffic_statistics' disabled  - "
             "for enabling check the trigger YAML")

    warnings.warn(message=DEPRECATION_MSG, category=DeprecationWarning)

    return

### MOVED
def clear_traffic_statistics(section, clear_stats_time=30):

    # Init
    log.info(banner("processor: 'clear_traffic_statistics'"))

    warnings.warn(message=DEPRECATION_MSG, category=DeprecationWarning)

    if _get_connection_class(section) == 'GenieTgn':
        return _clear_traffic_statistics_tcl(section)
    else:
        return _clear_traffic_statistics(section, clear_stats_time=clear_stats_time)

### MOVED
def _clear_traffic_statistics(section, clear_stats_time=30):

    '''Trigger Pre-Processor:
        * Clear statistics on TGN device before execution of a trigger
        * Controlled via section parameters provided in the triggers datafile
    '''

    # Check if user has disabled all traffic prcoessors with 'check_traffic'
    if 'check_traffic' in section.parameters and\
       section.parameters['check_traffic'] is False:
        # User has elected to disable execution of this processor
        log.info("SKIP: Processor 'clear_traffic_statistics' skipped - "
                 "parameter 'check_traffic' set to False in trigger YAML")
        return

    # Check if user wants to disable only 'clear_traffic_statistics' processor
    if 'clear_traffic_statistics' in section.parameters and\
       section.parameters['clear_traffic_statistics'] is False:
        # User has elected to disable execution of this processor
        log.info("SKIP: Processor 'clear_traffic_statistics' skipped - parameter"
                 " 'clear_traffic_statistics' set to False in trigger YAML")
        return

    # Find TGN devices
    tgn_devices = section.parameters['testbed'].find_devices(type='tgn')
    if not tgn_devices:
        log.info("SKIP: Traffic generator devices not found in testbed YAML")
        return

    for dev in tgn_devices:
        if dev.name not in section.parent.mapping_data['devices']:
            log.info("Traffic generator devices not specified in --devices")
            return

        # Connect to TGN
        if not dev.is_connected():
            try:
                dev.connect(via='tgn')
            except GenieTgnError as e:
                log.error(e)
                section.failed("Unable to connect to traffic generator device "
                               "'{}'".format(dev.name))
            else:
                log.info("Successfully connected to traffic generator device "
                         "'{}'".format(dev.name))

        # Clear traffic statistics
        try:
            dev.clear_statistics(wait_time=clear_stats_time)
        except GenieTgnError as e:
            log.error(e)
            section.failed("Unable to clear traffic statistics on traffic "
                           "generator device '{}'".format(dev.name))
        else:
            log.info("Cleared traffic statistics on traffic generator device "
                     "'{}'".format(dev.name))

### MOVED
def _clear_traffic_statistics_tcl(section):

    '''Trigger Pre-Processor:
        * Clear statistics on TGN device before execution of a trigger
        * Controlled via section parameters provided in the triggers datafile
    '''

    # Check disable processor
    if 'check_traffic' in section.parameters and\
       section.parameters['check_traffic'] is False:
        # User has elected to disable execution of this processor
        log.info("SKIP: Processor 'clear_traffic_statistics' skipped - "
                 "parameter 'check_traffic' set to False in trigger YAML")
        return

    # Get parameters from trigger
    tgn_max_outage_ms = section.parameters.get('tgn_max_outage_ms', None)

    # Get TGN devices from testbed
    testbed = section.parameters['testbed']

    for dev in testbed.find_devices(type='tgn'):

        # Set TGN device
        tgn_device = dev

        # Check if device is found in mapping context
        if not hasattr(section.parent, 'mapping_data') or\
           tgn_device.name not in section.parent.mapping_data['devices']:
            log.info("TGN '{}' information not found in mapping datafile".\
                     format(tgn_device.name))
            return

        # Check if TGN is connected
        if not tgn_device.is_connected():
            log.info("TGN '{}' not connected.".format(tgn_device.name))
            return

        # Set connection alias
        tgn_alias = getattr(tgn_device,
            section.parent.mapping_data['devices'][tgn_device.name]['context'])

        if tgn_max_outage_ms:
            try:
                tgn_alias.clear_stats()
            except GenieTgnError as e:
                log.error("Unable to clear traffic generator statistics",
                                from_exception=e)


# ==============================================================================
# processor: check_traffic_loss
# ==============================================================================

### MOVED
def check_traffic_loss(section, max_outage=120, loss_tolerance=15,
    rate_tolerance=2, check_interval=60, check_iteration=10,
    stream_settings='', clear_stats=False,
    clear_stats_time=30, pre_check_wait=''):

    # Init
    log.info(banner("processor: 'check_traffic_loss'"))

    warnings.warn(message=DEPRECATION_MSG, category=DeprecationWarning)

    if _get_connection_class(section) == 'GenieTgn':
        return _check_traffic_loss_tcl(section)
    else:
        return _check_traffic_loss(section, max_outage=max_outage,
                                   loss_tolerance=loss_tolerance,
                                   rate_tolerance=rate_tolerance,
                                   check_interval=check_interval,
                                   check_iteration=check_iteration,
                                   stream_settings=stream_settings,
                                   clear_stats=clear_stats,
                                   clear_stats_time=clear_stats_time,
                                   pre_check_wait=pre_check_wait)

### MOVED
def _check_traffic_loss(section, max_outage=120, loss_tolerance=15,
    rate_tolerance=2, check_interval=60, check_iteration=10,
    stream_settings='', clear_stats=False,
    clear_stats_time=30, pre_check_wait=''):

    '''Trigger Post-Processor:
        * Check traffic loss after trigger execution
        * Controlled via section parameters provided in the trigger datafile
    '''

    # Check if user has disabled all traffic prcoessors with 'check_traffic'
    if 'check_traffic' in section.parameters and\
       section.parameters['check_traffic'] is False:
        # User has elected to disable execution of this processor
        log.info("SKIP: Processor 'check_traffic_loss' skipped - "
                 "parameter 'check_traffic' set to False in trigger YAML")
        return

    # Check if user wants to disable only 'check_traffic_loss' processor
    if 'check_traffic_loss' in section.parameters and\
       section.parameters['check_traffic_loss'] is False:
        # User has elected to disable execution of this processor
        log.info("SKIP: Processor 'check_traffic_loss' skipped - parameter "
                 "'check_traffic_loss' set to False in trigger YAML")
        return

    # Find TGN devices
    tgn_devices = section.parameters['testbed'].find_devices(type='tgn')
    if not tgn_devices:
        log.info("SKIP: Traffic generator devices not found in testbed YAML")
        return

    for dev in tgn_devices:
        if dev.name not in section.parent.mapping_data['devices']:
            log.info("Traffic generator devices not specified in --devices")
            return

        # Connect to TGN
        if not dev.is_connected():
            try:
                dev.connect(via='tgn')
            except GenieTgnError as e:
                log.error(e)
                section.failed("Unable to connect to traffic generator device "
                               "'{}'".format(dev.name))
            else:
                log.info("Successfully connected to traffic generator device "
                         "'{}'".format(dev.name))

        # Check if user provided stream information
        streams_dict = {}
        if stream_settings:
            streams_dict = unpickle_stream_data(file=stream_settings, copy=True,
                                                copy_file='{}_stream_data'.\
                                                format(section.uid.strip('.uut')))
            # Print to logs
            log.info("User has provided outage/tolerance values for the following streams:")
            for stream in streams_dict['traffic_streams']:
                log.info("-> {}".format(stream))
            # Check if streams passed in are valid
            for stream in streams_dict['traffic_streams']:
                if stream not in dev.get_traffic_stream_names():
                    log.error("WARNING: Traffic item '{}' was not found in "
                              "configuration but provided in traffic streams "
                              " YAML".format(stream))

        # Check for traffic loss
        log.info("Checking for traffic outage/loss on all configured traffic streams")
        try:
            dev.check_traffic_loss(max_outage=max_outage,
                                   loss_tolerance=loss_tolerance,
                                   rate_tolerance=rate_tolerance,
                                   check_iteration=check_iteration,
                                   check_interval=check_interval,
                                   outage_dict=streams_dict,
                                   clear_stats=clear_stats,
                                   clear_stats_time=clear_stats_time,
                                   pre_check_wait=pre_check_wait)
        except GenieTgnError as e:
            log.error(e)
            section.failed("Traffic outage/loss observed for configured "
                           "traffic streams.")
        else:
            log.info("Traffic outage/loss is within expected thresholds for "
                     "all traffic streams.")

### MOVED
def _check_traffic_loss_tcl(section):

    '''Trigger Post-Processor:
        * Check traffic loss after trigger execution
        * Controlled via section parameters provided in the triggers datafile
    '''

    # Check disable processor
    if 'check_traffic' in section.parameters and\
       section.parameters['check_traffic'] is False:
        # User has elected to disable execution of this processor
        log.info("SKIP: Processor 'check_traffic_loss' skipped - "
                 "parameter 'check_traffic' set to False in trigger YAML")
        return

    # Get parameters from trigger
    traffic_loss = False
    delay = section.parameters.get('tgn_delay', 10)
    tgn_max_outage = section.parameters.get('tgn_max_outage', 60)
    tgn_max_outage_ms = section.parameters.get('tgn_max_outage_ms', None)
    tgn_resynch_traffic = section.parameters.get('tgn_resynch_traffic', True)

    # Get TGN devices from testbed
    testbed = section.parameters['testbed']

    for dev in testbed.find_devices(type='tgn'):

        # Set TGN device
        tgn_device = dev

        # Check if device is found in mapping context
        if not hasattr(section.parent, 'mapping_data') or \
           tgn_device.name not in section.parent.mapping_data['devices']:
            log.info("TGN '{}' information not found in mapping datafile".\
                     format(tgn_device.name))
            return

        # Check if TGN is connected
        if not tgn_device.is_connected():
            log.info("TGN '{}' not connected.".format(tgn_device.name))
            return

        # Set connection alias
        tgn_alias = getattr(tgn_device,
            section.parent.mapping_data['devices'][tgn_device.name]['context'])

        # Check for traffic loss
        log.info(banner("Check for traffic loss"))

        if tgn_max_outage_ms:
            try:
                log.info("Verify traffic outage")
                # Traffic loss is not expected beyond max_outage seconds
                tgn_alias.\
                    calculate_absolute_outage(max_outage_ms=tgn_max_outage_ms)
                log.info("PASS: Traffic stats OK")
            except GenieTgnError:
                traffic_loss = True
        else:
            try:
                # Verify traffic is restored within timeout if there is a loss
                tgn_alias.\
                    poll_traffic_until_traffic_resumes(timeout=tgn_max_outage,
                                                    delay_check_traffic=delay)
                log.info("PASS: Traffic stats OK")
            except GenieTgnError:
                traffic_loss = True

        # Traffic loss observed
        if traffic_loss:
            log.error("FAIL: Traffic stats are showing failure")
            # Resynch traffic stats to steady state
            if tgn_resynch_traffic:
                log.info("Traffic loss is seen and re-synch traffic now")
                try:
                    tgn_alias.get_reference_packet_rate()
                    log.info("PASS: Traffic stats initialized - steady state "
                             "reached after Re-synch")
                except GenieTgnError:
                    log.error("FAIL: Traffic stats initialized - steady state "
                              "not reached after Re-synch")

            # Fail the processor so that the trigger reports a 'fail'
            section.failed()


# ==============================================================================
# processor: compare_traffic_profile
# ==============================================================================

### DEMO
def compare_traffic_profile(section, clear_stats=True, clear_stats_time=30,
    view_create_interval=30, view_create_iteration=10, loss_tolerance=1,
    rate_tolerance=2, section_profile=''):

    '''Trigger Post-Processor:
        * Create a traffic profile
        * Compare it to 'golden' traffic profile created in common_setup (if executed)
        * Compare it to trigger's golden profile (if provided)
    '''

    log.info(banner("processor: 'compare_traffic_profile'"))

    warnings.warn(message=DEPRECATION_MSG, category=DeprecationWarning)

    # Check if user has disabled all traffic prcoessors with 'check_traffic'
    if 'check_traffic' in section.parameters and\
       section.parameters['check_traffic'] is False:
        # User has elected to disable execution of this processor
        log.info("SKIP: Processor 'compare_traffic_profile' skipped - "
                 "parameter 'check_traffic' set to False in trigger YAML")
        return

    # Check if user wants to disable only 'compare_traffic_profile' processor
    if 'compare_traffic_profile' in section.parameters and\
       section.parameters['compare_traffic_profile'] is False:
        # User has elected to disable execution of this processor
        log.info("SKIP: Processor 'compare_traffic_profile' skipped - parameter"
                 " 'compare_traffic_profile' set to False in trigger YAML")
        return

    if _get_connection_class(section) == 'GenieTgn':
        log.info("SKIP: Processor not supported for Ixia statictgn connection"
                 " implementation")
        return

    # Find TGN devices
    tgn_devices = section.parameters['testbed'].find_devices(type='tgn')
    if not tgn_devices:
        log.info("SKIP: Traffic generator devices not found in testbed YAML")
        return

    # Init
    for dev in tgn_devices:
        if dev.name not in section.parent.mapping_data['devices']:
            log.info("Traffic generator devices not specified in --devices")
            return

        # Connect to TGN
        if not dev.is_connected():
            try:
                dev.connect(via='tgn')
            except GenieTgnError as e:
                log.error(e)
                section.failed("Unable to connect to traffic generator device "
                               "'{}'".format(dev.name))
            else:
                log.info("Successfully connected to traffic generator device "
                         "'{}'".format(dev.name))

        # Create traffic profile
        try:
            section.tgn_profile = dev.create_traffic_streams_table(
                                    clear_stats=clear_stats,
                                    clear_stats_time=clear_stats_time,
                                    view_create_interval=view_create_interval,
                                    view_create_iteration=view_create_iteration)
        except GenieTgnError as e:
            log.error(e)
            section.failed("Unable to create traffic profile of configured "
                           "streams on traffic generator device '{}'".\
                           format(dev.name))
        else:
            log.info("Created traffic profile of configured streams on traffic "
                     "generator device '{}'".format(dev.name))

        # Copy traffic profile to runtime logs
        try:
            pickle_traffic(tgn_profile=section.tgn_profile,
                           tgn_profile_name='{}_traffic_profile'.\
                           format(section.uid.strip('.uut')))
        except Exception as e:
            log.error(e)
            section.failed("Error while saving section golden traffic profile "
                           "to runtime logs")
        else:
            log.info("Saved traffic profile to runtime logs")

        # Compare current traffic profile to section's golden traffic profile
        if section_profile:
            log.info("Comparing current traffic profile to user provided "
                     "golden traffic for section '{}'".format(section.uid))
            try:
                unpicked_section_profile = unpickle_traffic(section_profile)
            except Exception as e:
                log.error(e)
                section.failed("Error unpacking golden traffic profile into "
                               "table format")
            else:
                log.info("User provided golden profile:")
                log.info(unpicked_section_profile)

            # Compare profiles
            try:
                dev.compare_traffic_profile(profile1=section.tgn_profile,
                                            profile2=unpicked_section_profile,
                                            loss_tolerance=loss_tolerance,
                                            rate_tolerance=rate_tolerance)
            except GenieTgnError as e:
                log.error(e)
                section.failed("Comparison between current traffic profile and "
                               "section golden traffic profile failed")
            else:
                log.info("Comparison between current traffic profile and "
                         "section golden traffic profile passed")

        # Compare current traffic profile to common_setup generated golden traffic profile
        else:
            log.info("Comparing current traffic profile with golden traffic "
                     "profile generated in common_setup: profile_traffic subsection")

            # Compare it to common_setup golden profile
            if dev.get_golden_profile().field_names:
                try:
                    dev.compare_traffic_profile(profile1=section.tgn_profile,
                                                profile2=dev.get_golden_profile(),
                                                loss_tolerance=loss_tolerance,
                                                rate_tolerance=rate_tolerance)
                except GenieTgnError as e:
                    log.error(e)
                    section.failed("Comparison between current traffic profile "
                                   "and common_setup:profile_traffic failed")
                else:
                    log.info("Comparison between current traffic profile "
                             "and common_setup:profile_traffic passed")
            else:
                log.info("SKIP: Comparison of current traffic profile "
                         "with common setup traffic profile skipped."
                         "\n'common setup:profile_traffic' has not been "
                         "executed.")


# ==============================================================================
# processor: connect_traffic_device
# ==============================================================================

### MOVED
def connect_traffic_device(section, wait_time=30):

    '''Trigger Processor:
        * Connects to traffic generator device
    '''

    # Init
    log.info(banner("processor: 'connect_traffic_device'"))

    warnings.warn(message=DEPRECATION_MSG, category=DeprecationWarning)

    # Find TGN devices
    tgn_devices = section.parameters['testbed'].find_devices(type='tgn')
    if not tgn_devices:
        log.info("SKIP: Traffic generator devices not found in testbed YAML")
        return

    for dev in tgn_devices:
        if dev.name not in section.parent.mapping_data['devices']:
            log.info("Traffic generator devices not specified in --devices")
            return

        # Connect to TGN
        try:
            dev.connect(via='tgn')
        except GenieTgnError as e:
            log.error(e)
            section.failed("Unable to connect to traffic generator device "
                           "'{}'".format(dev.name))
        else:
            log.info("Connected to traffic generator device '{}'".\
                     format(dev.name))


# ==============================================================================
# processor: disconnect_traffic_device
# ==============================================================================

### MOVED
def disconnect_traffic_device(section, wait_time=30):

    '''Trigger Processor:
        * Disconnect from traffic generator device
    '''

    # Init

    log.info(banner("processor: 'disconnect_traffic_device'"))

    warnings.warn(message=DEPRECATION_MSG, category=DeprecationWarning)

    # Find TGN devices
    tgn_devices = section.parameters['testbed'].find_devices(type='tgn')
    if not tgn_devices:
        log.info("SKIP: Traffic generator devices not found in testbed YAML")
        return
    for dev in tgn_devices:
        if dev.name not in section.parent.mapping_data['devices']:
            log.info("Traffic generator devices not specified in --devices")
            return

        # Connect to TGN
        try:
            dev.disconnect()
        except GenieTgnError as e:
            log.error(e)
            section.failed("Unable to disconnect from traffic generator "
                           "device '{}'".format(dev.name))
        else:
            log.info("Disconnected from traffic generator device '{}'".\
                     format(dev.name))


# ==============================================================================
# processor: start_traffic
# ==============================================================================

### MOVED
def start_traffic(section, wait_time=30):

    '''Trigger Processor:
        * Starts traffic on traffic generator device
    '''

    # Init

    log.info(banner("processor: 'start_traffic'"))

    warnings.warn(message=DEPRECATION_MSG, category=DeprecationWarning)

    # Find TGN devices
    tgn_devices = section.parameters['testbed'].find_devices(type='tgn')
    if not tgn_devices:
        log.info("SKIP: Traffic generator devices not found in testbed YAML")
        return
    for dev in tgn_devices:
        if dev.name not in section.parent.mapping_data['devices']:
            log.info("Traffic generator devices not specified in --devices")
            return

        # Connect to TGN
        try:
            dev.connect(via='tgn')
        except GenieTgnError as e:
            log.error(e)
            section.failed("Unable to connect to traffic generator device "
                           "'{}'".format(dev.name))
        else:
            log.info("Successfully connected to traffic generator device "
                     "'{}'".format(dev.name))

        # Start traffic on TGN
        try:
            dev.start_traffic(wait_time=wait_time)
        except GenieTgnError as e:
            log.error(e)
            section.failed("Unable to start traffic on '{}'".format(dev.name))
        else:
            log.info("Started traffic on '{}'".format(dev.name))


# ==============================================================================
# processor: stop_traffic
# ==============================================================================
### MOVED
def stop_traffic(section, wait_time=30):

    '''Trigger Processor:
        * Stops traffic on traffic generator device
    '''

    # Init

    log.info(banner("processor: 'stop_traffic'"))

    warnings.warn(message=DEPRECATION_MSG, category=DeprecationWarning)

    # Find TGN devices
    tgn_devices = section.parameters['testbed'].find_devices(type='tgn')
    if not tgn_devices:
        log.info("SKIP: Traffic generator devices not found in testbed YAML")
        return

    for dev in tgn_devices:
        if dev.name not in section.parent.mapping_data['devices']:
            log.info("Traffic generator devices not specified in --devices")
            return

        # Connect to TGN
        try:
            dev.connect(via='tgn')
        except GenieTgnError as e:
            log.error(e)
            section.failed("Unable to connect to traffic generator device "
                           "'{}'".format(dev.name))
        else:
            log.info("Successfully connected to traffic generator device "
                     "'{}'".format(dev.name))

        # Stop traffic on TGN
        try:
            dev.stop_traffic(wait_time=wait_time)
        except GenieTgnError as e:
            log.error(e)
            section.failed("Unable to stop traffic on '{}'".format(dev.name))
        else:
            log.info("Stopped traffic on '{}'".format(dev.name))


# ==============================================================================
# processor: save_running_configuration
# ==============================================================================

### MOVED ###
def save_running_configuration(section, devices=None, copy_to_standby=False):

    '''Trigger Pre-Processor:
        * Save running configuration to bootflash:
    '''

    # Init
    log.info(banner("processor: 'save_running_configuration'"))

    warnings.warn(message=DEPRECATION_MSG, category=DeprecationWarning)

    # Init
    section.trigger_config = {}

    # Execute on section devices if devices list not specified
    if not devices:
        devices = [section.parameters['uut'].name]

    for dev in devices:
        device = section.parameters['testbed'].devices[dev]
        # Abstract
        lookup = Lookup.from_device(device, packages={'sdk':sdk})
        restore = lookup.sdk.libs.abstracted_libs.restore.Restore()

        # Get default directory
        save_dir = getattr(section.parent, 'default_file_system', {})
        if not save_dir or dev not in save_dir:
            section.parent.default_file_system = {}
            section.parent.default_file_system[device.name] = lookup.sdk.libs.abstracted_libs.subsection.get_default_dir(device=device)
            save_dir = section.parent.default_file_system

        # Save configuration to default directory
        try:
            section.trigger_config[device.name] = restore.save_configuration(device=device, method='config_replace',
                abstract=lookup, default_dir=save_dir, copy_to_standby=copy_to_standby)
        except Exception as e:
            log.error(e)
            section.failed("Unable to save running-configuration to device")
        else:
            log.info("Saved running-configuration to device")


# ==============================================================================
# processor: restore_running_configuration
# ==============================================================================

### MOVED ###
def restore_running_configuration(section, devices=None, iteration=10,
    interval=60, compare=False, compare_exclude=[], reload_timeout=1200):

    '''Trigger Pre-Processor:
        * Restore running configuration from bootflash:
    '''

    log.info(banner("processor: 'restore_running_configuration'"))

    warnings.warn(message=DEPRECATION_MSG, category=DeprecationWarning)

    # Execute on section devices if devices list not specified
    if not devices:
        devices = [section.parameters['uut'].name]

    for dev in devices:
        device = section.parameters['testbed'].devices[dev]
        # Abstract
        lookup = Lookup.from_device(device, packages={'sdk':sdk})
        restore = lookup.sdk.libs.abstracted_libs.restore.Restore()

        if hasattr(section, 'trigger_config'):
            restore.to_url = section.trigger_config[device.name]
        else:
            section.failed("processor: 'save_running_configuration' not "
                           "executed before running processor: "
                           "'restore_running_configuration'")

        # Restore configuration from default directory
        try:
            restore.restore_configuration(device=device, method='config_replace',
                                          abstract=lookup, iteration=iteration,
                                          interval=interval, compare=compare,
                                          compare_exclude=compare_exclude, reload_timeout=reload_timeout)
        except Exception as e:
            log.error(e)
            section.failed("Unable to restore running-configuration from device")
        else:
            log.info("Restored running-configuration from device")


# ==============================================================================
# processor: clear_logging
# ==============================================================================

### MOVED
def clear_logging(section, devices=None):

    '''Trigger Pre-Processor:
        * Clear logging on device
    '''

    # Init
    log.info(banner("processor: 'clear_logging'"))

    warnings.warn(message=DEPRECATION_MSG, category=DeprecationWarning)

    # Execute on section devices if devices list not specified
    if not devices:
        devices = [section.parameters['uut'].name]

    for dev in devices:
        device = section.parameters['testbed'].devices[dev]
        # Abstract
        lookup = Lookup.from_device(device, packages={'sdk':sdk})
        clear_log = lookup.sdk.libs.abstracted_libs.clear_logging.ClearLogging()

        # Clear logging on device
        try:
            log.info("Clear logging on device {}".format(dev))
            clear_log.clear_logging(device)
        except Exception as e:
            log.error(e)
            section.failed("Unable to clear logging on device")
        else:
            log.info("Cleared logging successfully on device")


# ==============================================================================
# processor: execute_command
# ==============================================================================
### MOVED
def pre_execute_command(section, devices=None, sleep_time=0, max_retry=1):
    '''Trigger Processor:
            * execute command
        '''
    # Init
    log.info(banner("processor: 'execute_command'"))

    warnings.warn(message=DEPRECATION_MSG, category=DeprecationWarning)

    sleep_if_cmd_executed = False
    for dev in devices:
        if dev == 'uut':
            device = section.parameters['uut']
        else:
            device = section.parameters['testbed'].devices.get(dev, None)
        # if device not in TB or not connected, then skip
        if not device or not device.is_connected():
            continue
        # execute list of commands given in yaml
        for cmd in devices[dev].get('cmds', []):
            if not cmd.get('condition') or section.result in list(map(TestResult.from_str,
                                                                      cmd['condition'])):
                exec_cmd = cmd.get('cmd', '')
                pattern = cmd.get('pattern', '')
                answer = cmd.get('answer', '')
                cmd_sleep = cmd.get('sleep', 0)
                cmd_timeout = cmd.get('timeout', 60)

                for _ in range(max_retry+1):
                    try:
                        # handle prompt if pattern and answer is in the datafile
                        if pattern:
                            if isinstance(pattern, str):
                                pattern = [pattern]
                            statement_list = []
                            for p in pattern:
                                statement_list.append(
                                    Statement(pattern=p,
                                              action='sendline({})'.format(answer),
                                              loop_continue=True,
                                              continue_timer=False))
                            dialog = Dialog(statement_list)
                            device.execute(exec_cmd, reply=dialog, timeout=cmd_timeout)
                        else:
                            device.execute(exec_cmd, timeout=cmd_timeout)
                    except SubCommandFailure as e:
                        log.error('Failed to execute "{cmd}" on device {d}: {e}'.format(cmd=exec_cmd,
                                                                                        d=device.name,
                                                                                        e=str(e)))

                        device.destroy()
                        log.info('Trying to recover after execution failure')
                        connect_device(device)
                    else:
                        log.info(
                            "Successfully executed command '{cmd}' device {d}".format(
                                cmd=exec_cmd,
                                d=device.name))
                        # sleep if any command is successfully executed
                        sleep_if_cmd_executed = True
                        break
                # didn't break loop, which means command execution is failed
                else:
                    section.failed('Reached max number of {} retries, command '
                                   'execution have failed'.format(max_retry))
                # if sleep is under the command, sleep after execution
                if cmd_sleep:
                    log.info("Sleeping for {sleep_time} seconds".format(
                        sleep_time=cmd_sleep))
                    time.sleep(cmd_sleep)

    if sleep_time and sleep_if_cmd_executed:
        log.info("Sleeping for {sleep_time} seconds".format(sleep_time=sleep_time))
        time.sleep(sleep_time)

### MOVED
def post_execute_command(section, devices=None, sleep_time=0, max_retry=1):
    '''Trigger Processor:
            * execute command
        '''
    # Init
    log.info(banner("processor: 'execute_command'"))

    warnings.warn(message=DEPRECATION_MSG, category=DeprecationWarning)

    sleep_if_cmd_executed = False
    for dev in devices:
        if dev == 'uut':
            device = section.parameters['uut']
        else:
            device = section.parameters['testbed'].devices.get(dev, None)
        # if device not in TB or not connected, then skip
        if not device or not device.is_connected():
            continue
        # execute list of commands given in yaml
        for cmd in devices[dev].get('cmds', []):
            if not cmd.get('condition') or section.result in list(map(TestResult.from_str,
                                                                      cmd['condition'])):
                exec_cmd = cmd.get('cmd', '')
                pattern = cmd.get('pattern', '')
                answer = cmd.get('answer', '')
                cmd_sleep = cmd.get('sleep', 0)
                cmd_timeout = cmd.get('timeout', 60)

                for _ in range(max_retry+1):
                    try:
                        # handle prompt if pattern and answer is in the datafile
                        if pattern:
                            if isinstance(pattern, str):
                                pattern = [pattern]
                            statement_list = []
                            for p in pattern:
                                statement_list.append(
                                    Statement(pattern=p,
                                              action='sendline({})'.format(answer),
                                              loop_continue=True,
                                              continue_timer=False))
                            dialog = Dialog(statement_list)
                            device.execute(exec_cmd, reply=dialog, timeout=cmd_timeout)
                        else:
                            device.execute(exec_cmd, timeout=cmd_timeout)
                    except SubCommandFailure as e:
                        log.error('Failed to execute "{cmd}" on device {d}: {e}'.format(cmd=exec_cmd,
                                                                                        d=device.name,
                                                                                        e=str(e)))

                        device.destroy()
                        log.info('Trying to recover after execution failure')
                        connect_device(device)
                    else:
                        log.info(
                            "Successfully executed command '{cmd}' device {d}".format(
                                cmd=exec_cmd,
                                d=device.name))
                        # sleep if any command is successfully executed
                        sleep_if_cmd_executed = True
                        break
                # didn't break loop, which means command execution is failed
                else:
                    section.failed('Reached max number of {} retries, command '
                                   'execution have failed'.format(max_retry))
                # if sleep is under the command, sleep after execution
                if cmd_sleep:
                    log.info("Sleeping for {sleep_time} seconds".format(
                        sleep_time=cmd_sleep))
                    time.sleep(cmd_sleep)

    if sleep_time and sleep_if_cmd_executed:
        log.info("Sleeping for {sleep_time} seconds".format(sleep_time=sleep_time))
        time.sleep(sleep_time)


# ==============================================================================
# processor: skip_setup_if_stable
# ==============================================================================
### MOVED
def pre_skip_setup_if_stable(section):
    params = section.parent.parameters

    warnings.warn(message=DEPRECATION_MSG, category=DeprecationWarning)

    # Check if last section was passed
    if ('previous_section_result' in params and
            params['previous_section_result'] == Passed):

        # Get function decorated by aetest.setup
        for item in section:
            if (hasattr(item, 'function') and
                    hasattr(item.function, '__testcls__') and
                    item.function.__testcls__ == SetupSection):

                # Save function so we dont have to find it during post
                params['section_setup_func'] = \
                    getattr(section, item.uid).__func__

                # affix skip decorator to setup_func
                skip.affix(section=params['section_setup_func'],
                           reason='Previous trigger passed. Device still '
                                  'in good state. No need to re-configure.')

                # Can only have one setup section per trigger
                break

### MOVED
def post_skip_setup_if_stable(section):
    params = section.parent.parameters
    params['previous_section_result'] = section.result

    warnings.warn(message=DEPRECATION_MSG, category=DeprecationWarning)

    if ('section_setup_func' in params and
            hasattr(params['section_setup_func'], '__processors__')):
        getattr(params['section_setup_func'], '__processors__').clear()

### MOVED
def skip_by_defect_status(section, defect_id, status=['R']):

    warnings.warn(message=DEPRECATION_MSG, category=DeprecationWarning)

    if not status:
        status = ['R']
    url = 'http://wwwin-metrics.cisco.com/cgi-bin/ws/ws_ddts_query_new.cgi/ws/ws_ddts_query_new.cgi?expert=_id:{}&type=json'.format(defect_id)
    try:
        if not defect_id:
            raise Exception('The defect id is not provided.')
        request = requests.get(url, timeout=29)
        if not request.ok:
            raise Exception('The website is unreachable due to {}'.format(request.reason))
        value = request.json()
        if not value:
            raise Exception('the defect id does not exist')
    except Exception as e:
        e = 'Timeout occurred. If you are an external user you cannot use this processor in your datafile.' if  isinstance(e, requests.exceptions.ReadTimeout) \
            else str(e)
        log.error(e)
    else:
        if value[0]['Status'] not in status:
            section.skipped('The section skipped since the defect_id provided ({}) has an inappropriate status'.format(defect_id))

# ==============================================================================
# PLEASE DON'T ADD PROCESSOR HERE
# PLEASE ADD TO `genie.libs.sdk.libs.abstracted_libs.processors` INSTEAD
# ==============================================================================