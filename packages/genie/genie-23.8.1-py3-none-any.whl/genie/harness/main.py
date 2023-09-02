import os
import sys
import logging
import argparse
import importlib

from pyats import log
from pyats.log import warnings
from pyats.datastructures.logic import logic_str

from pyats import aetest
from pyats.aetest.main import AEtest
from pyats.aetest import executer, runtime
from pyats.aetest.reporter import StandaloneReporter
from pyats.aetest.steps import Steps
from pyats.aetest.utils.pause import PauseOnPhrase
from pyats.easypy.tasks import Task

from .discovery import GenieScriptDiscover, GenieCommonSetupDiscover,\
                       GenieCommonCleanupDiscover, GenieTestcasesDiscover
from .loader import GenieLoader
from .utils import get_url


# module level logger
logger = logging.getLogger(__name__)

# declare module as infra
__genie_infra__ = True

CLI_DESCRIPTION = '''\

--------------------------------------------------------------------------------
'''


class Genie(AEtest):

    def run(self,
            testable,
            uid = None,
            reporter = None,
            # BEGIN DEPRECATING CODE
            ids = None,
            # END DEPRECATING CODE
            uids = None,
            groups = None,
            pdb = False,
            step_debug = None,
            loglevel = logging.INFO,
            random = False,
            random_seed = None,
            max_failures = None,
            pause_on = None,
            datafile = None,
            # Genie arguments
            pts_golden_config=None,
            pts_features='',
            trigger_datafile=None,
            # Datafiles
            pts_datafile=None,
            verification_datafile=None,
            parallel_verifications=None,
            # uids to execute
            verification_uids=None,
            trigger_uids=None,
            verification_groups=None,
            trigger_groups=None,
            config_datafile=None,
            mapping_datafile=None,
            subsection_datafile=None,
            debug_plugin=None,
            filetransfer_protocol=None,
            # -----------------------------------------------
            #               TCL TGN ARGUMENTS
            # -----------------------------------------------
            tgn_skip_configuration = False,
            tgn_enable = True,
            tgn_traffic_convergence_threshold = 60.0,
            tgn_reference_rate_threshold = 100.0,
            tgn_first_sample_threshold = 15.0,
            tgn_disable_traffic_post_execution = False,
            tgn_traffic_loss_recovery_threshold = 5.0,
            tgn_traffic_loss_tolerance_percentage = 15.0,
            tgn_enable_traffic_loss_check = True,
            tgn_config_post_device_config = True,
            tgn_profile_snapshot_threshold = 1200.0,
            tgn_routing_threshold = 120.0,
            tgntcl_enable_arp = False,
            tgntcl_learn_after_n_samples = 1,
            tgntcl_stream_sample_rate_percentage = 10.0,
            tgntcl_wait_multiplier = 1,
            # -----------------------------------------------
            #               PYTHON TGN ARGUMENTS
            # -----------------------------------------------
            tgn_port_list='',
            tgn_disable_load_configuration=False,
            tgn_disable_assign_ports=False,
            tgn_load_configuration_time=60,
            tgn_assign_ports_time=30,
            tgn_disable_start_protocols=False,
            tgn_protocols_convergence_time=120,
            tgn_stop_protocols_time=30,
            tgn_disable_regenerate_traffic=True,
            tgn_regenerate_traffic_time=30,
            tgn_disable_apply_traffic=False,
            tgn_apply_traffic_time=60,
            tgn_disable_send_arp=False,
            tgn_arp_wait_time=60,
            tgn_disable_send_ns=False,
            tgn_ns_wait_time=60,
            tgn_disable_start_traffic=False,
            tgn_steady_state_convergence_time=15,
            tgn_stop_traffic_time=15,
            tgn_remove_configuration=False,
            tgn_remove_configuration_time=30,
            tgn_disable_clear_statistics=False,
            tgn_clear_stats_time=15,
            tgn_disable_check_traffic_loss=False,
            tgn_traffic_outage_tolerance=120,
            tgn_traffic_loss_tolerance=15,
            tgn_traffic_rate_tolerance=5,
            tgn_check_traffic_streams=[],
            tgn_traffic_streams_data=None,
            tgn_stabilization_interval=60,
            tgn_stabilization_iteration=10,
            tgn_golden_profile=None,
            tgn_disable_profile_clear_stats=False,
            tgn_view_create_interval=30,
            tgn_view_create_iteration=10,
            tgn_disable_tracking_filter=False,
            tgn_disable_port_pair_filter=False,
            tgn_profile_traffic_loss_tolerance=2,
            tgn_profile_rate_loss_tolerance=2,
            tgn_logfile='tgn.log',
            processors = None,
            devices=None,
            **script_args):

        '''run test engine

        main API that runs a given testable. A testable can be a python AEtest
        script file, a script module (pre-loaded), or a pre-loaded module name.

        Arguments
        ---------
            testable    (obj): testable object, either path to a file, a module,
                               or a module name.
            uid     (TestableId): uid of this task, assigned by Easypy
            reporter  (BaseRootReporter): any reporter object that inherits the
                                          BaseRootReporter class.
            uids    (callable): callable, called with each section uid to test
                                if that section is to be run
            groups  (callable): callable, called with each testcase's groups to
                                test if that section is to be run
            pdb (bool): start the interactive debugger on failures/errors
            step_debug  (dict): dict of step_debug information
            loglevel    (level): logging level for this module
            random (bool): Boolean specifying whether to execute triggers
                           in random order.
            random_seed (int): Seeding integer used to randomize the
                               triggers. Use this to repeat a previously
                               randomized run.
            max_failures (int): number of maximum failure in a testscript before
                                aborting script run
            script_args (script_args): key/value of all other arguments to
                                       be passed to script level as script args.
            pause_on (string): Path to the yaml file or a string in dictionary
                               format that holds phrases, testcases, stopper
                               type and timeout values
            datafile (string): path to input datafile (yaml) that contains
                               script/testcase section data & features
            trigger_datafile (string): path to input datafile (yaml) that
                                       contains trigger information
            verification_datafile (string): path to input datafile (yaml) that
                                            contains verification information
            pts_datafile (string): path to input datafile (yaml) that
                                   contains pts information
            pts_features (list): List of pts_features to learn
            pts_golden_config (string): path to the pts_golden_config file
            trigger_uids (str) : string, will be parsed to list or logic
                                 callable, called with each trigger
                                 to test if that trigger is to be run
            trigger_groups (callable) : Callable, called with each triggers
                                        groups to test if that trigger is to
                                        be run
            verification_uids (str) : string, will be parsed to list or logic
                                      callable, called with each
                                      verification to test if that
                                      verification should be run
            verification_groups (callable) : Callable called with each
                                             verification to test if that
                                             verification should be run
            mapping_datafile (yaml): Mapping of device with appropriate
                                     connection alias.
            subsection_datafile (string): path to input datafile (yaml) that
                                       contains Common_(setup/cleanup)
                                       subsection information
            debug_plugin (string): Path of debug plugin
            filetransfer_protocol (string): File transfer protocol to be used
                                            during the run
            devices (list): List of the devices to connect to
                            (No mapping_datafile case)
            processors (dict): global pre/post/exception processors for this run
        '''
        # save arguments to self
        self.testable = testable
        self.uids = uids
        # In this case, we always want groups to be None,
        # And force verifications/triggers groups to be used instead
        self.groups = None
        self.pdb = pdb
        self.step_debug = step_debug
        self.loglevel = loglevel
        self.random = random
        self.random_seed = random_seed
        self.max_failures = max_failures
        self.pause_on = pause_on
        self.datafile = datafile
        self.trigger_datafile = trigger_datafile
        self.verification_datafile = verification_datafile
        self.pts_datafile = pts_datafile
        self.pts_features = pts_features
        self.pts_golden_config = pts_golden_config
        self.verification_uids = verification_uids
        self.trigger_uids = trigger_uids
        self.verification_groups = verification_groups
        self.trigger_groups = trigger_groups
        self.config_datafile = config_datafile
        self.mapping_datafile = mapping_datafile
        self.subsection_datafile = subsection_datafile
        self.debug_plugin = debug_plugin
        self.filetransfer_protocol = filetransfer_protocol
        self.devices = devices
        self.processors = processors or {}
        self.parallel_verifications = parallel_verifications
        # -----------------------------------------------
        #               TCL TGN ARGUMENTS
        # -----------------------------------------------
        self.tgn_skip_configuration = tgn_skip_configuration
        self.tgn_enable = tgn_enable
        self.tgn_traffic_convergence_threshold = tgn_traffic_convergence_threshold
        self.tgn_reference_rate_threshold = tgn_reference_rate_threshold
        self.tgn_first_sample_threshold = tgn_first_sample_threshold
        self.tgn_disable_traffic_post_execution = tgn_disable_traffic_post_execution
        self.tgn_traffic_loss_recovery_threshold = tgn_traffic_loss_recovery_threshold
        self.tgn_traffic_loss_tolerance_percentage = tgn_traffic_loss_tolerance_percentage
        self.tgn_enable_traffic_loss_check = tgn_enable_traffic_loss_check
        self.tgn_config_post_device_config = tgn_config_post_device_config
        self.tgn_profile_snapshot_threshold = tgn_profile_snapshot_threshold
        self.tgn_routing_threshold = tgn_routing_threshold
        self.tgntcl_enable_arp = tgntcl_enable_arp
        self.tgntcl_learn_after_n_samples = tgntcl_learn_after_n_samples
        self.tgntcl_stream_sample_rate_percentage = tgntcl_stream_sample_rate_percentage
        self.tgntcl_wait_multiplier = tgntcl_wait_multiplier
        # -----------------------------------------------
        #               PYTHON TGN ARGUMENTS
        # -----------------------------------------------
        self.tgn_port_list = tgn_port_list
        self.tgn_disable_load_configuration = tgn_disable_load_configuration
        self.tgn_disable_assign_ports = tgn_disable_assign_ports
        self.tgn_load_configuration_time = tgn_load_configuration_time
        self.tgn_assign_ports_time = tgn_assign_ports_time
        self.tgn_disable_start_protocols = tgn_disable_start_protocols
        self.tgn_protocols_convergence_time = tgn_protocols_convergence_time
        self.tgn_stop_protocols_time = tgn_stop_protocols_time
        self.tgn_disable_regenerate_traffic = tgn_disable_regenerate_traffic
        self.tgn_regenerate_traffic_time = tgn_regenerate_traffic_time
        self.tgn_disable_apply_traffic = tgn_disable_apply_traffic
        self.tgn_apply_traffic_time = tgn_apply_traffic_time
        self.tgn_disable_send_arp = tgn_disable_send_arp
        self.tgn_arp_wait_time = tgn_arp_wait_time
        self.tgn_disable_send_ns = tgn_disable_send_ns
        self.tgn_ns_wait_time = tgn_ns_wait_time
        self.tgn_disable_start_traffic = tgn_disable_start_traffic
        self.tgn_steady_state_convergence_time = tgn_steady_state_convergence_time
        self.tgn_stop_traffic_time = tgn_stop_traffic_time
        self.tgn_remove_configuration = tgn_remove_configuration
        self.tgn_remove_configuration_time = tgn_remove_configuration_time
        self.tgn_disable_clear_statistics = tgn_disable_clear_statistics
        self.tgn_clear_stats_time = tgn_clear_stats_time
        self.tgn_disable_check_traffic_loss = tgn_disable_check_traffic_loss
        self.tgn_traffic_outage_tolerance = tgn_traffic_outage_tolerance
        self.tgn_traffic_loss_tolerance = tgn_traffic_loss_tolerance
        self.tgn_traffic_rate_tolerance = tgn_traffic_rate_tolerance
        self.tgn_stabilization_interval = tgn_stabilization_interval
        self.tgn_check_traffic_streams = tgn_check_traffic_streams
        self.tgn_traffic_streams_data = tgn_traffic_streams_data
        self.tgn_stabilization_iteration = tgn_stabilization_iteration
        self.tgn_golden_profile = tgn_golden_profile
        self.tgn_disable_profile_clear_stats = tgn_disable_profile_clear_stats
        self.tgn_view_create_interval = tgn_view_create_interval
        self.tgn_view_create_iteration = tgn_view_create_iteration
        self.tgn_disable_tracking_filter = tgn_disable_tracking_filter
        self.tgn_disable_port_pair_filter = tgn_disable_port_pair_filter
        self.tgn_profile_traffic_loss_tolerance = tgn_profile_traffic_loss_tolerance
        self.tgn_profile_rate_loss_tolerance = tgn_profile_rate_loss_tolerance
        self.tgn_logfile = tgn_logfile
        # parse cli arguments, if any
        # this action also updates self.__dict__
        cliargs = self.parse_args()
        # argument priority:
        #   allow cli arguments to overwrite existing call arguments to run()
        #
        # priority:
        #       1. cliargs
        #       2. args to run()
        #       3. defaults
        self.__dict__.update(cliargs)

        # to support both list and logic string input
        if isinstance(self.trigger_uids, str):
            try:
                self.trigger_uids = logic_str(self.trigger_uids)
            except Exception as e:
                self.trigger_uids = self.trigger_uids.split()

        if isinstance(self.verification_uids, str):
            try:
                self.verification_uids = logic_str(self.verification_uids)
            except Exception as e:
                self.verification_uids = self.verification_uids.split()

        # Workaround for S3
        try:
            self.trigger_datafile = cliargs['trigger_file']
            self.verification_datafile = cliargs['verification_file']
        except:
            pass
       
        # set the log level for aetest module
        self.configure_logging()

        # Get corresponding url,  either devnet or internal
        url = get_url()

        # Using passed reporter or default standalone reporter
        if reporter:
            self.reporter = reporter
        else:
            self.reporter = StandaloneReporter()

        # reset executer to initial state
        executer.reset()
        
        # Update executer runtime arguments.
        executer.uids = self.uids
        executer.groups = self.groups
        executer.pdb = self.pdb
        executer.max_failures = self.max_failures

        # configure pause on phrase
        # -------------------------
        try:
            PauseOnPhrase.init(pause_on = self.pause_on)

        except Exception:
            logger.exception('Caught error while loading pause on phrase '
                             'input %s' % self.pause_on)
            return

        # configure step debug
        # --------------------
        try:
            Steps.init(stepDebugFile = self.step_debug,
                       testable = self.testable)

        except Exception:
            logger.exception('Caught error while loading step debug '
                             'file %s ' % self.step_debug)
            return


        # run the script
        # --------------
        # load the testable into TestScript object
        loader = GenieLoader()
        testscript = loader.load(self.testable, uid=uid, reporter=self.reporter)

        # Store datafiles to be used at a later time
        testscript.datafile = self.datafile
    
        # Convert to Genie tb
        # Convert mapping datafile into yaml
        # Set labels and set the mapping
        script_args['testbed'] = testscript.organize_testbed(\
                                        testbed=script_args['testbed'],
                                        mapping_datafile=self.mapping_datafile,
                                        devices=self.devices)

        # Load the datafiles
        testscript.load_genie_datafiles(testbed=script_args['testbed'],
                datafile=self.datafile,
                verification_datafile=self.verification_datafile,
                trigger_datafile=self.trigger_datafile,
                pts_datafile=self.pts_datafile,
                config_datafile=self.config_datafile,
                subsection_datafile=self.subsection_datafile)

        # Modify uids and groups if not provided by cli args or job file and
        # one exists in the datafiles
        self.trigger_uids = self.trigger_uids or testscript.triggers.get('uids')
        self.trigger_groups = self.trigger_groups or testscript.triggers.get('groups')
        self.verification_uids = self.verification_uids or\
                                 testscript.verifications.get('uids')
        self.verification_groups = self.verification_groups or\
                                 testscript.verifications.get('groups')

        # Save the file now and unpickle later
        testscript.pts_golden_config = \
                                    self.pts_golden_config

        testscript.debug_plugin = self.debug_plugin

        # set randomization
        # -----------------
        testscript.randomize(flag = self.random,
                                seed = self.random_seed)
       
        # if argument is False/not passed, but 1+ verfs set for parallel run,
        # then we should still use parallel_verifications
        if not self.parallel_verifications and hasattr(testscript, 'verifications'):
            self.parallel_verifications = any(
                value.get('parallel_verifications', False) 
                for key, value in testscript.verifications.items())

        # TODO: Check why raise, when the other are return
        # Those could probably disapear when Discovery handle uids/groups
        if self.trigger_uids and not callable(self.trigger_uids)\
            and not isinstance(self.trigger_uids, list):
            raise TypeError('trigger_uids must be a callable object')
        if self.verification_uids and not\
            callable(self.verification_uids)\
            and not isinstance(self.verification_uids, list):
            raise TypeError('verification_uids must be a callable object')
        if self.trigger_groups and not callable(self.trigger_groups):
            raise TypeError('trigger_groups must be a callable object')
        if self.verification_groups and\
            not callable(self.verification_groups):
            raise TypeError('verification_groups must be a callable '
                            'object')

        # Both _uids and _groups will be accepted and do double filter
        testscript.verification_uids = self.verification_uids
        testscript.verification_groups = self.verification_groups
        testscript.trigger_uids = self.trigger_uids
        testscript.trigger_groups = self.trigger_groups

        testscript.uids = self.uids
        testscript.groups = self.groups
        testscript.pts_features = self.pts_features
        testscript.config_datafile = self.config_datafile
        testscript.filetransfer_protocol = self.filetransfer_protocol
        testscript.url = url

        # update global processors
        testscript.processors.prepend(**self.processors)

        # Set the execution mode 
        testscript.parallel_verifications = self.parallel_verifications

        # -----------------------------------------------
        #               LEGACY TGN ARGUMENTS
        # -----------------------------------------------
        tgn_dict = {}
        tgn_dict['tgn_skip_configuration'] = self.tgn_skip_configuration
        tgn_dict['tgn_enable'] = self.tgn_enable
        tgn_dict['tgn_traffic_convergence_threshold'] = self.tgn_traffic_convergence_threshold
        tgn_dict['tgn_reference_rate_threshold'] = self.tgn_reference_rate_threshold
        tgn_dict['tgn_first_sample_threshold'] = self.tgn_first_sample_threshold
        tgn_dict['tgn_disable_traffic_post_execution'] = self.tgn_disable_traffic_post_execution
        tgn_dict['tgn_traffic_loss_recovery_threshold'] = self.tgn_traffic_loss_recovery_threshold
        tgn_dict['tgn_traffic_loss_tolerance_percentage'] = self.tgn_traffic_loss_tolerance_percentage
        tgn_dict['tgn_enable_traffic_loss_check'] = self.tgn_enable_traffic_loss_check
        tgn_dict['tgn_config_post_device_config'] = self.tgn_config_post_device_config
        tgn_dict['tgn_profile_snapshot_threshold'] = self.tgn_profile_snapshot_threshold
        tgn_dict['tgn_routing_threshold'] = self.tgn_routing_threshold
        tgn_dict['tgn_port_list'] = self.tgn_port_list
        tgn_dict['tgn_arp_wait_time'] = self.tgn_arp_wait_time
        tgn_dict['tgntcl_enable_arp'] = self.tgntcl_enable_arp
        tgn_dict['tgntcl_learn_after_n_samples'] = self.tgntcl_learn_after_n_samples
        tgn_dict['tgntcl_stream_sample_rate_percentage'] = self.tgntcl_stream_sample_rate_percentage
        tgn_dict['tgntcl_wait_multiplier'] = self.tgntcl_wait_multiplier
        testscript.tgn_keys = tgn_dict

        # -----------------------------------------------
        #               PYTHON TGN ARGUMENTS
        # -----------------------------------------------
        testscript.tgn_port_list = self.tgn_port_list
        testscript.tgn_disable_load_configuration = self.tgn_disable_load_configuration
        testscript.tgn_disable_assign_ports = self.tgn_disable_assign_ports
        testscript.tgn_load_configuration_time = self.tgn_load_configuration_time
        testscript.tgn_assign_ports_time = self.tgn_assign_ports_time
        testscript.tgn_disable_start_protocols = self.tgn_disable_start_protocols
        testscript.tgn_protocols_convergence_time = self.tgn_protocols_convergence_time
        testscript.tgn_stop_protocols_time = self.tgn_stop_protocols_time
        testscript.tgn_disable_regenerate_traffic = self.tgn_disable_regenerate_traffic
        testscript.tgn_regenerate_traffic_time = self.tgn_regenerate_traffic_time
        testscript.tgn_disable_apply_traffic = self.tgn_disable_apply_traffic
        testscript.tgn_apply_traffic_time = self.tgn_apply_traffic_time
        testscript.tgn_disable_send_arp = self.tgn_disable_send_arp
        testscript.tgn_arp_wait_time = self.tgn_arp_wait_time
        testscript.tgn_disable_send_ns = self.tgn_disable_send_ns
        testscript.tgn_ns_wait_time = self.tgn_ns_wait_time
        testscript.tgn_disable_start_traffic = self.tgn_disable_start_traffic
        testscript.tgn_steady_state_convergence_time = self.tgn_steady_state_convergence_time
        testscript.tgn_stop_traffic_time = self.tgn_stop_traffic_time
        testscript.tgn_remove_configuration = self.tgn_remove_configuration
        testscript.tgn_remove_configuration_time = self.tgn_remove_configuration_time
        testscript.tgn_disable_clear_statistics = self.tgn_disable_clear_statistics
        testscript.tgn_clear_stats_time = self.tgn_clear_stats_time
        testscript.tgn_disable_check_traffic_loss = self.tgn_disable_check_traffic_loss
        testscript.tgn_traffic_outage_tolerance = tgn_traffic_outage_tolerance
        testscript.tgn_traffic_loss_tolerance = self.tgn_traffic_loss_tolerance
        testscript.tgn_traffic_rate_tolerance = self.tgn_traffic_rate_tolerance
        testscript.tgn_stabilization_interval = self.tgn_stabilization_interval
        testscript.tgn_check_traffic_streams = self.tgn_check_traffic_streams
        testscript.tgn_traffic_streams_data = self.tgn_traffic_streams_data
        testscript.tgn_stabilization_iteration = self.tgn_stabilization_iteration
        testscript.tgn_golden_profile = self.tgn_golden_profile
        testscript.tgn_disable_profile_clear_stats = self.tgn_disable_profile_clear_stats
        testscript.tgn_view_create_interval = self.tgn_view_create_interval
        testscript.tgn_view_create_iteration = self.tgn_view_create_iteration
        testscript.tgn_disable_tracking_filter = self.tgn_disable_tracking_filter
        testscript.tgn_disable_port_pair_filter = self.tgn_disable_port_pair_filter
        testscript.tgn_profile_traffic_loss_tolerance = self.tgn_profile_traffic_loss_tolerance
        testscript.tgn_profile_rate_loss_tolerance = self.tgn_profile_rate_loss_tolerance
        testscript.tgn_logfile = self.tgn_logfile

        # run testscript
        # --------------
        # all script args are passed to testscript as parameters
        # when done, return result to caller

        # Set up the discoveries
        # Genie Modification
        # Call the correct discoveries
        #runtime.discoverer.script = GenieScriptDiscover
        runtime.discoverer.testcase = GenieTestcasesDiscover
        aetest.CommonSetup.discoverer = GenieCommonSetupDiscover
        aetest.CommonCleanup.discoverer = GenieCommonCleanupDiscover

        with testscript as script:
            result = testscript(**script_args)
            self.reporter.log_summary()
            return result

    def configure_parser(self, commandline, parser, legacy):
        '''configure cli parser

        configure and returns a parser that can parse sys.argv. This api takes
        care of two things:

            1. parse sys.args passed from upstream (easypy), where any arguments
               not parsed by easypy or the job file is passed-through to aetest
               and the script, and
            2. parse sys.argv when executing in command-line mode (outside of
               easypy environment)

        Arguments
        ---------
            commandline (bool): whether aetest was started from command line
            parser (argparse.ArgumentParser): parser object, or None
            legacy (bool): whether to use/support legacy CLI
        '''

        # create base parser, do not add help (add it later at the bottom)
        # Genie modification
        # Set up the parsers
        parser = super().configure_parser(commandline, parser, legacy)

        if legacy:
            trigger_datafile_opt = ['-trigger_datafile']
            verification_datafile_opt = ['-verification_datafile']
            trigger_file_opt = ['-trigger_file']
            verification_file_opt = ['-verification_file']
            pts_datafile_opt = ['-pts_datafile']
            pts_features_opt = ['-pts_features']
            pts_golden_config_opt = ['-pts_golden_config']
            config_datafile_opt = ['-config_datafile']
            verification_uids_opt = ['-verification_uids']
            trigger_uids_opt = ['-trigger_uids']
            verification_groups_opt = ['-verification_groups']
            trigger_groups_opt = ['-trigger_groups']
            mapping_datafile_opt = ['-mapping_datafile']
            subsection_datafile_opt = ['-subsection_datafile']
            debug_plugin_opt = ['-debug_plugin']
            devices_opt = ['-devices']
            filetransfer_protocol_opt = ['-filetransfer_protocol']
            parallel_verifications_opt =['-parallel_verifications']
            # ------------------------------------------------------------------
            #                       TCL TGN ARGUMENTS
            # ------------------------------------------------------------------
            tgn_skip_configuration_opt = ['-tgn_skip_configuration']
            tgn_enable_opt = ['-tgn_enable']
            tgn_traffic_convergence_threshold_opt = ['-tgn_traffic_convergence_threshold']
            tgn_reference_rate_threshold_opt = ['-tgn_reference_rate_threshold']
            tgn_first_sample_threshold_opt = ['-tgn_first_sample_threshold']
            tgn_disable_traffic_post_execution_opt = ['-tgn_disable_traffic_post_execution']
            tgn_traffic_loss_recovery_threshold_opt = ['-tgn_traffic_loss_recovery_threshold']
            tgn_traffic_loss_tolerance_percentage_opt = ['-tgn_traffic_loss_tolerance_percentage']
            tgn_enable_traffic_loss_check_opt = ['-tgn_enable_traffic_loss_check']
            tgn_config_post_device_config_opt = ['-tgn_config_post_device_config']
            tgn_profile_snapshot_threshold_opt = ['-tgn_profile_snapshot_threshold']
            tgn_routing_threshold_opt = ['-tgn_routing_threshold']
            tgntcl_enable_arp_opt = ['-tgntcl_enable_arp']
            tgntcl_learn_after_n_samples_opt = ['-tgntcl_learn_after_n_samples']
            tgntcl_stream_sample_rate_percentage_opt = ['-tgntcl_stream_sample_rate_percentage']
            tgntcl_wait_multiplier_opt = ['-tgntcl_wait_multiplier']
            # ------------------------------------------------------------------
            #                       PYTHON TGN ARGUMENTS
            # ------------------------------------------------------------------
            tgn_port_list_opt = ['-tgn_port_list']
            tgn_disable_load_configuration_opt = ['-tgn_disable_load_configuration']
            tgn_disable_assign_ports_opt = ['-tgn_disable_assign_ports']
            tgn_load_configuration_time_opt = ['-tgn_load_configuration_time']
            tgn_assign_ports_time_opt = ['-tgn-assign-ports-time']
            tgn_disable_start_protocols_opt = ['-tgn_disable_start_protocols']
            tgn_protocols_convergence_time_opt = ['-tgn_protocols_convergence_time']
            tgn_stop_protocols_time_opt = ['-tgn_stop_protocols_time']
            tgn_disable_regenerate_traffic_opt = ['-tgn_disable_regenerate_traffic']
            tgn_regenerate_traffic_time_opt = ['-tgn_regenerate_traffic_time']
            tgn_disable_apply_traffic_opt = ['-tgn_disable_apply_traffic']
            tgn_apply_traffic_time_opt = ['-tgn_apply_traffic_time']
            tgn_disable_send_arp_opt = ['-tgn_disable_send_arp']
            tgn_arp_wait_time_opt = ['-tgn_arp_wait_time']
            tgn_disable_send_ns_opt = ['-tgn_disable_send_ns']
            tgn_ns_wait_time_opt = ['-tgn_ns_wait_time']
            tgn_disable_start_traffic_opt = ['-tgn_disable_start_traffic']
            tgn_steady_state_convergence_time_opt = ['-tgn_steady_state_convergence_time']
            tgn_stop_traffic_time_opt = ['-tgn_stop_traffic_time']
            tgn_remove_configuration_opt = ['-tgn_remove_configuration']
            tgn_remove_configuration_time_opt = ['-tgn_remove_configuration_time']
            tgn_disable_clear_statistics_opt = ['-tgn_disable_clear_statistics']
            tgn_clear_stats_time_opt = ['-tgn_clear_stats_time']
            tgn_disable_check_traffic_loss_opt = ['-tgn_disable_check_traffic_loss']
            tgn_traffic_outage_tolerance_opt = ['-tgn_traffic_outage_tolerance']
            tgn_traffic_loss_tolerance_opt = ['-tgn_traffic_loss_tolerance']
            tgn_traffic_rate_tolerance_opt = ['-tgn_traffic_rate_tolerance']
            tgn_stabilization_interval_opt = ['-tgn_stabilization_interval']
            tgn_check_traffic_streams_opt = ['-tgn_check_traffic_streams']
            tgn_traffic_streams_data_opt = ['-tgn_traffic_streams_data']
            tgn_stabilization_iteration_opt = ['-tgn_stabilization_iteration']
            tgn_golden_profile_opt = ['-tgn_golden_profile']
            tgn_disable_profile_clear_stats_opt = ['-tgn_disable_profile_clear_stats']
            tgn_view_create_interval_opt = ['-tgn_view_create_interval']
            tgn_view_create_iteration_opt = ['-tgn_view_create_iteration']
            tgn_disable_tracking_filter_opt = ['-tgn_disable_tracking_filter']
            tgn_disable_port_pair_filter_opt = ['-tgn_disable_port_pair_filter']
            tgn_profile_traffic_loss_tolerance_opt = ['-tgn_profile_traffic_loss_tolerance']
            tgn_profile_rate_loss_tolerance_opt = ['-tgn_profile_rate_loss_tolerance']
            tgn_logfile_opt = ['-tgn_logfile']
        else:
            trigger_datafile_opt = ['--trigger-datafile']
            verification_datafile_opt = ['--verification-datafile']
            trigger_file_opt = ['--trigger-file']
            verification_file_opt = ['--verification-file']
            pts_datafile_opt = ['--pts-datafile']
            pts_features_opt = ['--pts-features']
            pts_golden_config_opt = ['--pts-golden-config']
            config_datafile_opt = ['--config-datafile']
            verification_uids_opt = ['--verification-uids']
            trigger_uids_opt = ['--trigger-uids']
            verification_groups_opt = ['--verification-groups']
            trigger_groups_opt = ['--trigger-groups']
            mapping_datafile_opt = ['--mapping-datafile']
            subsection_datafile_opt = ['--subsection-datafile']
            debug_plugin_opt = ['--debug-plugin']
            devices_opt = ['--devices']
            filetransfer_protocol_opt = ['--filetransfer-protocol']
            parallel_verifications_opt =['--parallel-verifications']
            # ------------------------------------------------------------------
            #                       TCL TGN ARGUMENTS
            # ------------------------------------------------------------------
            tgn_skip_configuration_opt = ['--tgn-skip-configuration']
            tgn_enable_opt = ['--tgn-enable']
            tgn_traffic_convergence_threshold_opt = ['--tgn-traffic-convergence-threshold']
            tgn_reference_rate_threshold_opt = ['--tgn-reference-rate-threshold']
            tgn_first_sample_threshold_opt = ['--tgn-first-sample-threshold']
            tgn_disable_traffic_post_execution_opt = ['--tgn-disable-traffic-post-execution']
            tgn_traffic_loss_recovery_threshold_opt = ['--tgn-traffic-loss-recovery-threshold']
            tgn_traffic_loss_tolerance_percentage_opt = ['--tgn-traffic-loss-tolerance-percentage']
            tgn_enable_traffic_loss_check_opt = ['--tgn-enable-traffic-loss-check']
            tgn_config_post_device_config_opt = ['--tgn-config-post-device-config']
            tgn_profile_snapshot_threshold_opt = ['--tgn-profile-snapshot-threshold']
            tgn_routing_threshold_opt = ['--tgn-routing-threshold']
            tgntcl_enable_arp_opt = ['--tgntcl-enable-arp']
            tgntcl_learn_after_n_samples_opt = ['--tgntcl-learn-after-n-samples']
            tgntcl_stream_sample_rate_percentage_opt = ['--tgntcl-stream-sample-rate-percentage']
            tgntcl_wait_multiplier_opt = ['--tgntcl-wait-multiplier']
            # ------------------------------------------------------------------
            #                       PYTHON TGN ARGUMENTS
            # ------------------------------------------------------------------
            tgn_port_list_opt = ['--tgn-port-list']
            tgn_disable_load_configuration_opt = ['--tgn-disable-load-configuration']
            tgn_disable_assign_ports_opt = ['--tgn-disable-assign-ports']
            tgn_load_configuration_time_opt = ['--tgn-load-configuration-time']
            tgn_assign_ports_time_opt = ['--tgn-assign-ports-time']
            tgn_disable_start_protocols_opt = ['--tgn-disable-start-protocols']
            tgn_protocols_convergence_time_opt = ['--tgn-protocols-convergence-time']
            tgn_stop_protocols_time_opt = ['--tgn-stop-protocols-time']
            tgn_disable_regenerate_traffic_opt = ['--tgn-disable-regenerate-traffic']
            tgn_regenerate_traffic_time_opt = ['--tgn-regenerate-traffic-time']
            tgn_disable_apply_traffic_opt = ['--tgn-disable-apply-traffic']
            tgn_apply_traffic_time_opt = ['--tgn-apply-traffic-time']
            tgn_disable_send_arp_opt = ['--tgn-disable-send-arp']
            tgn_arp_wait_time_opt = ['--tgn-arp-wait-time']
            tgn_disable_send_ns_opt = ['--tgn-disable-send-ns']
            tgn_ns_wait_time_opt = ['--tgn-ns-wait-time']
            tgn_disable_start_traffic_opt = ['--tgn-disable-start-traffic']
            tgn_steady_state_convergence_time_opt = ['--tgn-steady-state-convergence-time']
            tgn_stop_traffic_time_opt = ['--tgn-stop-traffic-time']
            tgn_remove_configuration_opt = ['--tgn-remove-configuration']
            tgn_remove_configuration_time_opt = ['--tgn-remove-configuration-time']
            tgn_disable_clear_statistics_opt = ['--tgn-disable-clear-statistics']
            tgn_clear_stats_time_opt = ['--tgn-clear-stats-time']
            tgn_disable_check_traffic_loss_opt = ['--tgn-disable-check-traffic-loss']
            tgn_traffic_outage_tolerance_opt = ['--tgn-traffic-outage-tolerance']
            tgn_traffic_loss_tolerance_opt = ['--tgn-traffic-loss-tolerance']
            tgn_traffic_rate_tolerance_opt = ['--tgn-traffic-rate-tolerance']
            tgn_stabilization_interval_opt = ['--tgn-stabilization-interval']
            tgn_check_traffic_streams_opt = ['--tgn-check-traffic-streams']
            tgn_traffic_streams_data_opt = ['--tgn-traffic-streams-data']
            tgn_stabilization_iteration_opt = ['--tgn-stabilization-iteration']
            tgn_golden_profile_opt = ['--tgn-golden-profile']
            tgn_disable_profile_clear_stats_opt = ['--tgn-disable-profile-clear-stats']
            tgn_view_create_interval_opt = ['--tgn-view-create-interval']
            tgn_view_create_iteration_opt = ['--tgn-view-create-iteration']
            tgn_disable_tracking_filter_opt = ['--tgn-disable-tracking-filter']
            tgn_disable_port_pair_filter_opt = ['--tgn-disable-port-pair-filter']
            tgn_profile_traffic_loss_tolerance_opt = ['--tgn-profile-traffic-loss-tolerance']
            tgn_profile_rate_loss_tolerance_opt = ['--tgn-profile-rate-loss-tolerance']
            tgn_logfile_opt = ['--tgn-logfile']

        group = parser.add_argument_group('Genie arguments')
        group.add_argument(*trigger_datafile_opt,
                           metavar='FILE',
                           type=str,
                           default=argparse.SUPPRESS,
                           help='Trigger configuration datafile')

        group.add_argument(*verification_datafile_opt,
                           metavar='FILE',
                           type=str,
                           default=argparse.SUPPRESS,
                           help='VerificationTrigger configuration datafile')

        group.add_argument(*trigger_file_opt,
                           metavar='FILE',
                           type=str,
                           default=argparse.SUPPRESS,
                           help='Trigger configuration file')

        group.add_argument(*verification_file_opt,
                           metavar='FILE',
                           type=str,
                           default=argparse.SUPPRESS,
                           help='VerificationTrigger configuration file')

        group.add_argument(*pts_datafile_opt,
                           metavar='FILE',
                           type=str,
                           default=argparse.SUPPRESS,
                           help='PTS configuration datafile')

        group.add_argument(*pts_features_opt,
                           type=str,
                           default=argparse.SUPPRESS,
                           help='Features to learn for pts')

        group.add_argument(*pts_golden_config_opt,
                           metavar='FILE',
                           type=str,
                           default=argparse.SUPPRESS,
                           help='Golden configuration file')

        group.add_argument(*config_datafile_opt,
                           metavar='FILE',
                           type=str,
                           default=argparse.SUPPRESS,
                           help='File containing configuration information')

        group.add_argument(*verification_uids_opt,
                           metavar = 'LOGIC',
                           type = str,
                           default=argparse.SUPPRESS,
                           help = "string matching verifications uids "
                                  "to run."
                                  "\neg: -uids=\"ospf bgp\""
                                  "\nor: -uids=\"And('.*ospf.*', 'bgp.+')\"")

        group.add_argument(*trigger_uids_opt,
                           metavar = 'LOGIC',
                           type = str,
                           default=argparse.SUPPRESS,
                           help = "string matching triggers uids to run."
                                  "\neg: -uids=\"ospf bgp\""
                                  "\nor: -uids=\"And('ospf', 'bgp.+')\"")

        group.add_argument(*verification_groups_opt,
                           metavar = 'LOGIC',
                           type = logic_str,
                           default=argparse.SUPPRESS,
                           help = "logic string matching verifications groups "
                                  "to be run.\n"
                                  "eg: -ids=\"And('sanity', 'regression')\"")

        group.add_argument(*trigger_groups_opt,
                           metavar = 'LOGIC',
                           type = logic_str,
                           default=argparse.SUPPRESS,
                           help = "logic string matching triggers groups "
                                  "to be run.\n"
                                  "eg: -ids=\"And('sanity', 'regression')\"")

        group.add_argument(*mapping_datafile_opt,
                           metavar='FILE',
                           type=str,
                           default=argparse.SUPPRESS,
                           help='File containing device to connection '
                                'mapping')

        group.add_argument(*subsection_datafile_opt,
                           metavar='FILE',
                           type=str,
                           default=argparse.SUPPRESS,
                           help='File containing Common_(setup/cleanup)'
                                'subsection information')

        group.add_argument(*debug_plugin_opt,
                           metavar='FILE',
                           type=str,
                           default=argparse.SUPPRESS,
                           help='File pointing to debug plugin')

        group.add_argument(*filetransfer_protocol_opt,
                           type=str,
                           default=argparse.SUPPRESS,
                           help='File transfer protocol to be used in the run')

        group.add_argument(*devices_opt,
                           type=str,
                           nargs='*',
                           default=argparse.SUPPRESS,
                           help='List of devices to connect to')
        
        group.add_argument(*parallel_verifications_opt,
                           action='store_true',
                           default=argparse.SUPPRESS,
                           help='Execute verifications in parallel')

        # ----------------------------------------------------------------------
        #                       PYTHON TGN ARGUMENTS
        # ----------------------------------------------------------------------

        # Genie TGN arguments
        group_tgn = parser.add_argument_group('Python Traffic Generator (TGN) Arguments')

        # tgn_port_list
        group_tgn.add_argument(*tgn_port_list_opt,
                               type=str,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='List of ports to connect to on TGN device.'
                                    '\nDefault: None')

        # tgn_disable_load_configuration
        group_tgn.add_argument(*tgn_disable_load_configuration_opt,
                               action="store_true",
                               default=argparse.SUPPRESS,
                               help='Disable loading config on TGN device.'
                                    '\nDefault: False')

        # tgn_disable_assign_ports
        group_tgn.add_argument(*tgn_disable_assign_ports_opt,
                               action="store_true",
                               default=argparse.SUPPRESS,
                               help='Disable assigning Ixia virtual ports to '
                                    'physical ports.\nDefault: False')

        # tgn_load_configuration_time
        group_tgn.add_argument(*tgn_load_configuration_time_opt,
                               type=int,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='Wait time after loading config on TGN '
                                    'device.\nDefault: 60 (seconds)')

        # tgn_assign_ports_time
        group_tgn.add_argument(*tgn_assign_ports_time_opt,
                               type=int,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='Wait time after assigning ports on TGN '
                                    'device.\nDefault: 30 (seconds)')

        # tgn_disable_start_protocols
        group_tgn.add_argument(*tgn_disable_start_protocols_opt,
                               action="store_true",
                               default=argparse.SUPPRESS,
                               help='Disable starting protocols/routing engine '
                                    'on TGN device.\nDefault: False')

        # tgn_protocols_convergence_time
        group_tgn.add_argument(*tgn_protocols_convergence_time_opt,
                               type=int,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='Wait time after starting protocols on TGN '
                                    'device.\nDefault: 120 (seconds)')

        # tgn_stop_protocols_time
        group_tgn.add_argument(*tgn_stop_protocols_time_opt,
                               type=int,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='Wait time after stopping protocols on TGN '
                                    'device.\nDefault: 30 (seconds)')

        # tgn_disable_regenerate_traffic
        group_tgn.add_argument(*tgn_disable_regenerate_traffic_opt,
                               action="store_true",
                               default=argparse.SUPPRESS,
                               help='Disable regenerating traffic streams '
                                    'after loading config.\nDefault: True')

        # tgn_regenerate_traffic_time
        group_tgn.add_argument(*tgn_regenerate_traffic_time_opt,
                               type=int,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='Wait time after regenerating single '
                                    'traffic stream on TGN device.'
                                    '\nDefault: 10 (seconds)')

        # tgn_disable_apply_traffic
        group_tgn.add_argument(*tgn_disable_apply_traffic_opt,
                               action="store_true",
                               default=argparse.SUPPRESS,
                               help='Disable applying traffic after loading '
                                    'config on TGN device.\nDefault: False')

        # tgn_apply_traffic_time
        group_tgn.add_argument(*tgn_apply_traffic_time_opt,
                               type=int,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='Wait time after applying traffic on TGN '
                                    'device.\nDefault: 60 (seconds)')

        # tgn_disable_send_arp
        group_tgn.add_argument(*tgn_disable_send_arp_opt,
                               action="store_true",
                               default=argparse.SUPPRESS,
                               help='Disable sending ARP to all interfaces on '
                                    'TGN device.\nDefault: False')

        # tgn_arp_wait_time
        group_tgn.add_argument(*tgn_arp_wait_time_opt,
                               type=int,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='Wait time after sending ARP to all '
                                    'interfaces on TGN device.'
                                    '\nDefault: 60 (seconds)')

        # tgn_disable_send_ns
        group_tgn.add_argument(*tgn_disable_send_ns_opt,
                               action="store_true",
                               default=argparse.SUPPRESS,
                               help='Disable sending NS to all interfaces on '
                                    'TGN device.\nDefault: False')

        # tgn_ns_wait_time
        group_tgn.add_argument(*tgn_ns_wait_time_opt,
                               type=int,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='Wait time after sending NS to all '
                                    'interfaces on TGN device.'
                                    '\nDefault: 60 (seconds)')

        # tgn_disable_start_traffic
        group_tgn.add_argument(*tgn_disable_start_traffic_opt,
                               action="store_true",
                               default=argparse.SUPPRESS,
                               help='Disable starting traffic on the TGN device.'
                                    '\nDefault: False')

        # tgn_steady_state_convergence_time
        group_tgn.add_argument(*tgn_steady_state_convergence_time_opt,
                               type=int,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='Wait time for traffic streams to coverge '
                                    'to steady state.\nDefault: 60 (seconds)')

        # tgn_stop_traffic_time
        group_tgn.add_argument(*tgn_stop_traffic_time_opt,
                               type=int,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='Wait time after stopping traffic on TGN '
                                    'device.\nDefault: 15 (seconds)')

        # tgn_remove_configuration
        group_tgn.add_argument(*tgn_remove_configuration_opt,
                               action="store_true",
                               default=argparse.SUPPRESS,
                               help='Remove config on TGN device after '
                                    'stopping traffic.\nDefault: False')

        # tgn_remove_configuration_time
        group_tgn.add_argument(*tgn_remove_configuration_time_opt,
                               type=int,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='Wait time after removing config from TGN '
                                    'device.\nDefault: 30 (seconds)')

        # tgn_disable_clear_statistics
        group_tgn.add_argument(*tgn_disable_clear_statistics_opt,
                               action="store_true",
                               default=argparse.SUPPRESS,
                               help='Disable clearing protocol/traffic '
                                    'statistics on TGN device.\nDefault: False')

        # tgn_clear_stats_time
        group_tgn.add_argument(*tgn_clear_stats_time_opt,
                               type=int,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='Wait time after clearing protocol/traffic '
                                    'statistics on TGN device.'
                                    '\nDefault: 15 (seconds)')

        # tgn_view_create_interval
        group_tgn.add_argument(*tgn_view_create_interval_opt,
                               type=int,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='Wait time between custom "GENIE" view '
                                    'recheck iteration.\nDefault: 30 (seconds)')

        # tgn_view_create_iteration
        group_tgn.add_argument(*tgn_view_create_iteration_opt,
                               type=int,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='Max number of attempts to verify custom '
                                    '"GENIE" view is populated.'
                                    '\nDefault: 10 attempts')

        # tgn_disable_tracking_filter
        group_tgn.add_argument(*tgn_disable_tracking_filter_opt,
                               action="store_true",
                               default=argparse.SUPPRESS,
                               help='Disable automatic enabling of \'Traffic '
                                    'Item\' tracking filter.'
                                    '\nDefault: False')

        # tgn_disable_port_pair_filter
        group_tgn.add_argument(*tgn_disable_port_pair_filter_opt,
                               action="store_true",
                               default=argparse.SUPPRESS,
                               help='Disable automatic enabling of \'Source/'
                                    'Dest Port Pair\' tracking filter.'
                                    '\nDefault: False')

        # tgn_disable_check_traffic_loss
        group_tgn.add_argument(*tgn_disable_check_traffic_loss_opt,
                               action="store_true",
                               default=argparse.SUPPRESS,
                               help='Disable checking for traffic outage/loss '
                                    'on TGN device.\nDefault: False')

        # tgn_traffic_outage_tolerance
        group_tgn.add_argument(*tgn_traffic_outage_tolerance_opt,
                               type=int,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='Max traffic outage for all traffic '
                                    'streams.\nDefault: 120 (seconds)')

        # tgn_traffic_loss_tolerance
        group_tgn.add_argument(*tgn_traffic_loss_tolerance_opt,
                               type=int,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='Max traffic \'Loss %%\' for all traffic '
                                    'streams.\nDefault: 15 %%')

        # tgn_traffic_rate_tolerance
        group_tgn.add_argument(*tgn_traffic_rate_tolerance_opt,
                               type=int,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='Max diff between \'Tx Rate\' and \'Rx '
                                    'Rate\' for all traffic streams.'
                                    '\nDefault: 5 pps')

        # tgn_check_traffic_streams
        group_tgn.add_argument(*tgn_check_traffic_streams_opt,
                               type=list,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='Custom list of traffic streams for traffic '
                                    'loss check.\nDefault: None')

        # tgn_traffic_streams_data
        group_tgn.add_argument(*tgn_traffic_streams_data_opt,
                               metavar='FILE',
                               type=str,
                               default=argparse.SUPPRESS,
                               help='Custom YAML file with stream specific '
                                    'tolerance values for traffic loss check.'
                                    '\nDefault: None')

        # tgn_stabilization_interval
        group_tgn.add_argument(*tgn_stabilization_interval_opt,
                               type=int,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='Wait time between traffic loss recheck '
                                    'iteration.\nDefault: 120 (seconds)')

        # tgn_stabilization_iteration
        group_tgn.add_argument(*tgn_stabilization_iteration_opt,
                               type=int,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='Max iteration to recheck traffic loss.'
                                    '\nDefault: 10')

        # tgn_disable_profile_clear_stats
        group_tgn.add_argument(*tgn_disable_profile_clear_stats_opt,
                               action="store_true",
                               default=argparse.SUPPRESS,
                               help='Disable clearing protocol/traffic '
                                    'statistics before creating traffic profile.'
                                    '\nDefault: False')

        # tgn_profile_traffic_loss_tolerance
        group_tgn.add_argument(*tgn_profile_traffic_loss_tolerance_opt,
                               type=int,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='Max \'Loss %%\' diff between 2 traffic '
                                    'profiles.\nDefault: 2%%')

        # tgn_profile_rate_loss_tolerance
        group_tgn.add_argument(*tgn_profile_rate_loss_tolerance_opt,
                               type=int,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='Maximum \'Tx Rate\' and \'Rx Rate\' diff '
                                    'between 2 traffic profiles.'
                                    '\nDefault: 5')

        # tgn_logfile
        group_tgn.add_argument(*tgn_logfile_opt,
                               type=str,
                               metavar='',
                               default=argparse.SUPPRESS,
                               help='TGN events log file.'
                                    '\nDefault: tgn.log')

        ########################################################################
        #                         TCL TGN ARGUMENTS                            #
        ########################################################################

        # TCL tgn group
        group_tcl_tgn = parser.add_argument_group('TCL Traffic Generator (TGN) Arguments')

        # tgn_skip_configuration
        group_tcl_tgn.add_argument(*tgn_skip_configuration_opt,
                           type=bool,
                           metavar='',
                           default=argparse.SUPPRESS,
                           help='Skip loading config on TGN device.'
                                '\nDefault: False')

        # tgn_enable
        group_tcl_tgn.add_argument(*tgn_enable_opt,
                           action='store_true',
                           default=argparse.SUPPRESS,
                           help='Enable common_setup subsection '
                                '\'initialize_traffic\'.\nDefault: False')

        # tgn_traffic_convergence_threshold
        group_tcl_tgn.add_argument(*tgn_traffic_convergence_threshold_opt,
                           type=float,
                           metavar='',
                           default=argparse.SUPPRESS,
                           help='Wait time for traffic streams to coverge to '
                                'steady state.\nDefault: 60 (seconds)')

        # tgn_reference_rate_threshold
        group_tcl_tgn.add_argument(*tgn_reference_rate_threshold_opt,
                           type=float,
                           metavar='',
                           default=argparse.SUPPRESS,
                           help='Wait time before checking traffic stream '
                                'rates for traffic profile.'
                                '\nDefault: 100 (seconds)')

        # tgn_first_sample_threshold
        group_tcl_tgn.add_argument(*tgn_first_sample_threshold_opt,
                           type=float,
                           metavar='',
                           default=argparse.SUPPRESS,
                           help='Wait time before collecting first sample '
                                'of traffic stream rates.'
                                '\nDefault: 15 (seconds)')

        # tgn_disable_traffic_post_execution
        group_tcl_tgn.add_argument(*tgn_disable_traffic_post_execution_opt,
                           type=bool,
                           metavar='',
                           default=argparse.SUPPRESS,
                           help='Stop traffic after Genie execution completes.'
                                '\nDefault: False')

        # tgn_traffic_loss_recovery_threshold
        group_tcl_tgn.add_argument(*tgn_traffic_loss_recovery_threshold_opt,
                           type=float,
                           metavar='',
                           default=argparse.SUPPRESS,
                           help='Wait time for traffic to reach steady state '
                                'during traffic loss check.\nDefault: 5 (seconds)')

        # tgn_traffic_loss_tolerance_percentage
        group_tcl_tgn.add_argument(*tgn_traffic_loss_tolerance_percentage_opt,
                           type=float,
                           metavar='',
                           default=argparse.SUPPRESS,
                           help='Max traffic \'Loss %%\'\nDefault: 15 %%')

        # tgn_enable_traffic_loss_check
        group_tcl_tgn.add_argument(*tgn_enable_traffic_loss_check_opt,
                           type=bool,
                           metavar='',
                           default=argparse.SUPPRESS,
                           help='Enable traffic loss checks.\nDefault: True')

        # tgn_config_post_device_config
        group_tcl_tgn.add_argument(*tgn_config_post_device_config_opt,
                           type=bool,
                           metavar='',
                           default=argparse.SUPPRESS,
                           help='Config TGN device *only* after device config '
                                'is successful.\nDefault: True')

        # tgn_profile_snapshot_threshold
        group_tcl_tgn.add_argument(*tgn_profile_snapshot_threshold_opt,
                           type=float,
                           metavar='',
                           default=argparse.SUPPRESS,
                           help='Wait time to collect reference rate for '
                                'traffic profile.\nDefault: 1200 (seconds)')

        # tgn_routing_threshold
        group_tcl_tgn.add_argument(*tgn_routing_threshold_opt,
                           type=float,
                           metavar='',
                           default=argparse.SUPPRESS,
                           help='Wait time after starting protocols & before '
                                'starting traffic.\nDefault: 120 (seconds)')

        ########################################################################
        #                         PSAT TGN ARGUMENTS                           #
        ########################################################################

        # tgntcl_enable_arp
        group_tcl_tgn.add_argument(*tgntcl_enable_arp_opt,
                           type=bool,
                           metavar='',
                           default=argparse.SUPPRESS,
                           help='Send ARP to TGN device')

        # tgntcl_learn_after_n_samples
        group_tcl_tgn.add_argument(*tgntcl_learn_after_n_samples_opt,
                           type=int,
                           metavar='',
                           default=argparse.SUPPRESS,
                           help='Create traffic profile after N number of samples.')

        # tgntcl_stream_sample_rate_percentage
        group_tcl_tgn.add_argument(*tgntcl_stream_sample_rate_percentage_opt,
                           type=float,
                           metavar='',
                           default=argparse.SUPPRESS,
                           help='Max %% tolerance between that 2 samples of '
                                'traffic stream.')

        # tgntcl_wait_multiplier
        group_tcl_tgn.add_argument(*tgntcl_wait_multiplier_opt,
                           type=int,
                           metavar='',
                           default=argparse.SUPPRESS,
                           help='Multiplier for arg '
                                '\'tgn_profile_snapshot_threshold\'.')
        return parser


def main(testable = '__main__', **kwargs):
    '''Shortcut call to run AEtest Main Program

    This is needed in order to stay compatible for test scripts to run as a
    standalone script without using the __main__ functionality.

    It simply wraps AEtest class to run with module name '__main__', and exit.


    Arguments
    ---------
        kwargs (dict): all arguments to this function will be passed through
                       to AEtest.runTests function.

    Example
    -------
        >>> if __name__ == '__main__':
        ...     aetest.main()
    '''
    return Genie().run(testable=testable, **kwargs)

# shortcut to run Genie
def gRun(testscript=None, *args, max_runtime = None, **kwargs):
    '''run api

    Shortcut function to start a Task(), wait for it to finish, and return
    the result to the caller. This api avoids the overhead of having to deal
    with the task objects, and provides a black-box method of creating tasks
    sequentially.

    Arguments
    ---------
        max_runtime (int): maximum time to wait for the task to run and
                           finish, before terminating it forcifully and
                           raising errors. If not provided, waits forever.
        args (tuple): any other positional argument to be passed to Task()
        kwargs (dict): any other keyword arguments to be passed to Task()

    Returns
    -------
        the task's result code
    '''
    assert testscript is None, "Genie does not require any 'testscript'"
    # Genie modification 
    test_path = os.path.dirname(os.path.abspath(__file__))
    testscript = os.path.join(test_path, 'genie_testscript.py')
    # Change the test_harness
    task = Task(testscript=testscript,
                test_harness='genie.harness',
                *args, **kwargs)
    task.start()
    task.wait(max_runtime)
    return task.result


class gTask:
    ''' Wrapper class for pyats.easypy.tasks.Task with
    genie testscript and harness.

    This is a multiprocessing.Process class and is used for
    multiprocessing to allow Genie tasks to execute in parallel.
    '''

    def __new__(self, *args, **kwargs):
        test_path = os.path.dirname(os.path.abspath(__file__))
        testscript = os.path.join(test_path, 'genie_testscript.py')
        task = Task(testscript=testscript,
                    test_harness='genie.harness',
                    *args, **kwargs)
        return task
