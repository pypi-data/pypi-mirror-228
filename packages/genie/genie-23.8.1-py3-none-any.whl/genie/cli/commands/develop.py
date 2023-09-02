'''
This file has a large test file that takes a long time to run. 
(tests/large_tests/develop_undevelop_test.py)
So, it is not included in the standard "make test" command.
To test this file (and undevelop.py), run "make largetest". 
'''

# Import Python packages
import os
import re
import sys
import copy
import json
import time
import yaml
import shutil
import logging
from pathlib import Path
from pkg_resources import working_set

# Import 3rd party packages
from prettytable import PrettyTable

# Import pyATS packages
from pyats.cli.utils import cmd
from pyats.log.utils import banner
from pyats.cli.base import Command
from pyats.log.colour import Palette, Style, FgColour

# Set up internal logger
log = logging.getLogger(__name__)


class DevelopCommand(Command):
    """
    Command to put pyATS packages into development mode
    """

    name = "develop"

    help = ("Puts desired pyATS packages into development mode")

    description = """
Puts listed pyATS packages into development mode. Listed packages will have 
their repositories downloaded from Github if required and 'make develop' will be 
run for each package. By default, internal Cisco repos will be cloned if the 
pyATS installation is internal, otherwise external repos will be cloned instead. 
Github SSH keys are required to clone internal Cisco packages."""

    usage = """pyats develop [packages...] [options]
  
Usage Examples:
  pyats develop all
  pyats develop genie.libs.sdk --skip-version-check
  pyats develop genie.libs.parser genie.trafficgen --external
  pyats develop unicon.plugins genie.libs --delete-repos --directory my_repos
  pyats develop pyats.config --clone-only"""

    # constants
    KEYBOARD_INTERRUPT_WAIT_TIME = 5
    GENIELIBS_FLAGS = {
        'dir_deleted': False,
        'repo_cloned': False,
        'deps_installed': False,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load repo data from accompanying data file
        parent_dir = Path(__file__).parent.absolute()
        datafile = os.path.join(parent_dir, 'git_repo_data.yaml')
        with open(datafile, 'r') as fd:
            self.pkg_data = yaml.safe_load(fd)

        self.pip_data = None 
        
        if self.parser.prog == 'pyats develop':
            self.parser.add_argument(
                'packages',
                type=str,
                nargs='*',
                help="Packages to put into development mode. Available choices:"
                     "\nall, {}".format(", ".join(self.pkg_data.keys())))

            self.parser.add_argument(
                '-e', '--external',
                action='store_true',
                help="Clone external public repositories instead of internal. "
                     "Only applicable to internal Cisco pyATS installations. "
                     "For external pyATS Installations, external public "
                     "repositories will always be used (Optional)")

            self.parser.add_argument(
                '-d', '--directory',
                type=str,
                default = '',
                help="Absolute or relative path of directory to clone "
                     "repositories into. If not supplied, then the default "
                     "directory is $VIRTUAL_ENV/pypi (Optional)")

            self.parser.add_argument(
                '-f', '--force-develop',
                action='store_true',
                help="Run 'make develop' even if packages are already in "
                     "development mode (Optional)")

            self.parser.add_argument(
                '-s', '--skip-version-check',
                action='store_true',
                help="Do not check if pyATS packages are up to date before tool"
                     " execution. WARNING: Using this option may lead to pyATS "
                     "package version conflicts which could result in a "
                     "corrupted pyATS installation! Use with discretion "
                     "(Optional)")

            limiter = self.parser.add_mutually_exclusive_group(required = False)

            limiter.add_argument(
                '--delete-repos',
                action='store_true',
                help="Delete existing repositories within directory before "
                     "cloning new ones (Optional) IMPORTANT: Please back up "
                     "your work before using this option!")

            limiter.add_argument(
                '-c', '--clone-only',
                action='store_true',
                help="Clone the repositories, but do not put any packages into "
                     "development mode (Optional)")

    def parse_args(self, argv):
        # inject general group options
        self.add_general_opts(self.parser)

        # do the parsing
        args, unknown = self.parser.parse_known_args(argv)
        sys.argv = sys.argv[:1]+unknown
        return args

    def is_internal_installation(self, working_set_list):
        if 'ats.cisco' in working_set_list:
            return True
        return False

    def rebuild_pkg_data(self, package_data, internal_installation): 
        """ Rebuilds pkg_data depending on type of installation. If internal, 
        then the ats.cisco.internal_data package will be accessed to get 
        internal metadata. Then uses a URL field in the pkg_data dictionary to 
        determine if the package is included. No URL, no access to that package
        """

        package_data_copy = copy.deepcopy(package_data)
        rebuilt_package_data_dict = dict()

        if internal_installation:
            from ats.cisco.internal_data import get_internal_package_metadata

            # Incorporate internal data into pkg_data
            internal_data = get_internal_package_metadata()
            for key1, value1 in internal_data.items():
                for key2, value2 in value1.items():
                    package_data_copy.setdefault(key1, {})[key2] = value2

        for key, value in package_data_copy.items():
            if 'url' in package_data_copy[key]:
                rebuilt_package_data_dict[key] = value

        return rebuilt_package_data_dict

    def check_requested_packages_validity(self, packages, pkg_data):
        """ Runs checks on requested packages to enforce correct usage"""

        # If no packages are provided, then blow up
        if len(packages) == 0:
            raise Exception("Please specify at least one package to put into "
                            "development mode \nFor help, enter the command: "
                            "'pyats develop --help'")

        # If a package name is invalid, then blow up
        for pkg in packages:
            if pkg not in pkg_data and pkg != 'all':
                raise Exception(
                    "Package {} is not an available choice for the current "
                    "installation mode. Please choose from one or more of the "
                    "following options: \n\n    {}".format(pkg,"\n    "
                    .join(['all'] + list(pkg_data.keys()))))

    def rebuild_package_list(self, requested_packages, pkg_data):
        """ Rebuids the requested package list. Expand 'all' and 'genie.libs' 
        into appropriate packages. Remove duplicates and sort list"""

        adjusted_list = list(requested_packages).copy()

        # Expand 'all' to be all pkgs in pkg_data dict (different results 
        # depending on if installation is internal or external)
        if 'all' in adjusted_list:
            adjusted_list = list(pkg_data.keys())

        # Expand 'genie.libs' to be all genie.libs packages (except parser)
        if 'genie.libs' in adjusted_list:
            adjusted_list.extend(pkg_data['genie.libs']['related_pkgs'])
            adjusted_list.remove('genie.libs')

        # Remove duplicate packages and sort for aethetics 
        adjusted_list = sorted(list(dict.fromkeys(adjusted_list)))
        log.info("Requested packages:\n  {}\n".format(', '
                                              .join(adjusted_list)))
        return adjusted_list

    def check_version(self):
        """Runs 'pyats version check --outdated'. Shows error msg if failure"""
        
        log.info("Ensuring you have the latest pyATS version. "
                 "Please be patient...\n")
        try:
            cmd("pyats version check --outdated", incl_stderr=False)
        except Exception:
            raise Exception("\nERROR: Not all pyATS packages are up to date. "
                            "Please run 'pyats version update' before using "
                            "this tool.") from None
        log.info("All packages are up to date!\n")

    def install_upgrade_pip_setuptools(self):
        """ Update pip and setuptools. This helps packages which need 
        latest/newest versions of these tools."""

        log.info("Upgrading pip and setuptools...")
        cmd("pip install --upgrade pip setuptools")

    def create_directory(self, directory):
        """ Makes a directory at the specified location including any required 
        parent directories """

        if not os.path.isabs(directory):
            directory = os.path.join(os.getcwd(), directory)
        try:
            os.makedirs(directory, exist_ok=True)
        except Exception as e:
            log.exception("Error during directory creation")
            if "Permission denied" in str(e):
                log.error(
                    "\nAn error has occured during creation of the following "
                    "directory:\n%s\nThis is likely due to incorrect/insuffient"
                    " directory permissions. \nPlease ensure that you have the "
                    "correct permissions to access this directory" 
                    % directory)
            raise
        return directory

    def delete_directory(self, directory, pkg):
        """ Deletes a directory at the specified location, including any files 
        and subdirectories within that directory"""
        
        # genie.libs packages are in same repo but are looped over individually
        # ensure the genielibs repo is not deleted between loops 
        if self.is_pkg_part_of_genielibs(pkg) \
                and self.GENIELIBS_FLAGS['dir_deleted']:
            log.debug("Genie.libs repo has already been deleted. "
                      "Skipping deletion of directory: %s" % directory)
            return

        try:
            shutil.rmtree(directory)
        except Exception as e:
            log.exception("Error during directory creation")
            if "Permission denied" in str(e):
                log.error(
                    "\nAn error has occured during deletion of the following "
                    "directory:\n%s\nThis is likely due to incorrect/insuffient"
                    " directory permissions. \nPlease ensure that you have the "
                    "correct permissions to permanently delete this directory" 
                    % directory)
            raise

        log.debug("%s deleted successfully.\n" % directory)
        if self.is_pkg_part_of_genielibs(pkg):
            self.GENIELIBS_FLAGS['dir_deleted'] = True

    def package_is_in_dev_mode(self, package_name):
        """ Returns True if package_name is in development mode. Checks pip list
        output as json and regex extracts package data """

        if self.pip_data is None:
            self.pip_data = {}
            cmd_output = cmd("pip list -e --format json")
            extracted_json = re.match(r'.*(\[[\s\S]+\]).*', cmd_output)
            if extracted_json:
                self.pip_data = json.loads(extracted_json.groups()[0])

        # package_name can be pyats for internal installations only and internal
        # installations have ats packages only
        if package_name == 'pyats':
            package_name = 'ats' 

        for pkg in self.pip_data:
            if pkg['name'] == package_name:
                return True
        return False

    def prepare_repo(self, pkg, pkg_data, repo_dir, delete_repos_flag):
        """ Prepares repository by cloning, deleting or doing nothing as 
        required """

        # If directory exists and if directory is not empty
        if os.path.isdir(repo_dir) and len(os.listdir(repo_dir)) != 0:
            log.debug("%s directory already exists and is not empty" % repo_dir)

            if delete_repos_flag:
                log.debug("Delete-repos option chosen. Deleting %s." % repo_dir)
                self.delete_directory(repo_dir, pkg)
                self.clone_repo(pkg, pkg_data, repo_dir)
            else:
                # If directory exists and is not empty and --delete-repos flag 
                # is not set, then assume directory is a package repo. If it 
                # isn't, then check_git_repo_validity() will catch it
                return
        else:
            self.clone_repo(pkg, pkg_data, repo_dir)

    def clone_repo(self, pkg, pkg_data, repo_dir):
        """ Clones repos with an extra (and hopefully helpful) error message """

        # genie.libs packages are in same repo but are looped over individually
        # ensure the genielibs repo is not cloned again between loops 
        if self.is_pkg_part_of_genielibs(pkg) \
                and self.GENIELIBS_FLAGS['repo_cloned']:
            log.debug("Genie.libs repo has already been cloned. "
                      "Skipping clone step for %s" % pkg)
            return False

        log.info("Cloning %s from %s" % (pkg, pkg_data[pkg]['url']))
        try:
            cmd("git clone %s %s" % (pkg_data[pkg]['url'], repo_dir))
        except Exception as e:
            log.exception("Error during 'git clone' process")
            if "Permission denied" in str(e):
                log.error(
                    "\nAn error has occured during the repository cloning "
                    "process for the %s package due to denied permission.\n"
                    "This could be due to incorrect or missing Github SSH "
                    "credentials or due to directory permission issues.\nPlease"
                    " ensure that:\n  -your Github profile has the correct "
                    "public SSH key for the device you are currently using\n  "
                    "-proper permissions exist for the %s directory.\n" 
                    % (pkg, repo_dir))
            raise
        else:
            log.debug("%s repository cloned successfully" 
                      % pkg_data[pkg]['repo_name'])
            if self.is_pkg_part_of_genielibs(pkg):
                self.GENIELIBS_FLAGS['repo_cloned'] = True
            return True

    def is_pkg_part_of_genielibs(self, pkg):
        return pkg.startswith('genie.libs') and pkg != 'genie.libs.parser'

    def check_git_repo_validity(self, repo_dir):
        """ Returns True if a .git folder exists in the specified directory """

        log.debug("Checking if .git folder exists in %s" % repo_dir)
        if os.path.isdir(os.path.join(repo_dir, ".git")):
            log.info("Repository location: %s" % repo_dir)
        else:
            raise Exception(
                "\n%s is a directory but it is not empty and it is not an "
                "existing repository.\nGit repos can only be cloned into an "
                "existing directory if the directory is empty.\n\nPlease empty "
                "the directory, specify a different directory using the "
                "--directory \nargument, or use the --delete-repos argument to "
                "permanently delete the directory before cloning.\n\n"
                % str(repo_dir))

    def run_make_develop(self, pkg, repo_dir):
        # Setup for 'make develop' section
        makefile_target = 'develop'
        makefile_dir = repo_dir

        # Use the custom make target for genie.libs packages to allow for
        # packages to be put into development mode individually
        if self.is_pkg_part_of_genielibs(pkg):
            self.install_genielibs_dependencies(makefile_dir)
            package_name = pkg.split('.')[-1]
            makefile_target = 'develop-' + package_name

        # yang.connector has a unique Makefile location
        if pkg == 'yang.connector':
            makefile_dir = os.path.join(repo_dir, 'connector')

        log.info("Running 'make develop' for %s" % pkg)
        cmd('make %s -C %s' % (makefile_target, makefile_dir))

    def install_genielibs_dependencies(self, makefile_dir):
        if not self.GENIELIBS_FLAGS['deps_installed']:
            log.info("Installing dependencies for genie.libs...")
            cmd("make dependencies -C %s" % makefile_dir)
            self.GENIELIBS_FLAGS['deps_installed'] = True
        else:
            log.info("Dependencies for genie.libs packages have already been "
                     "installed. Skipping 'make dependencies' for genie.libs")

    def show_keyboard_interrupt_warning_and_wait(self, sleep_time):
        log.warning(
            "\n\nKeyboardInterrupt detected!\n\nForcefully exiting program now "
            "could result in a corrupted pyATS installation!\n\nDevelopment "
            "mode process will restart interrupted step in %s seconds\n\n"
            "If you're sure you want to exit, then press Ctrl+C again "
            "before execution resumes.\n\n" % sleep_time)
        time.sleep(sleep_time)

    def reinsert_genielibs_pkgs(self, cur_pkg, packages, successful_packages):
        # If user interupts execution while a genielibs package is being put 
        # into development mode, then add back in all previously executed 
        # genielibs packages as the repo directory may be deleted when execution 
        # resumes. Corner case code but keeps pyATS working if user interrupts
        ret_list = list(packages).copy()
        ret_list.insert(0, cur_pkg)
        for i in range(len(successful_packages)):
            pkg = successful_packages[i]
            if self.is_pkg_part_of_genielibs(pkg):
                ret_list.insert(0, pkg)

        successful_packages = [x for x in successful_packages if not 
            self.is_pkg_part_of_genielibs(x)]

        # Sort and remove duplicates 
        ret_list = sorted(list(dict.fromkeys(ret_list)))
        return ret_list, successful_packages

    def show_results(self, sucessful_package_list, failed_package_list):
        """ Searches through packages and shows package info if package is part 
            of sucessful_package_list"""

        all_packages = sucessful_package_list + failed_package_list

        # List the packages that have been successfully put into dev mode
        if not len(all_packages):
            log.info("This tool's execution has not put any packages into or "
                     "removed any packages from development mode.")
            return

        if 'pyats' in sucessful_package_list:
            sucessful_package_list.remove('pyats')
            sucessful_package_list.extend(
                list(self.pkg_data['pyats']['related_pkgs']))

        # Use/print a nice table for results 
        t = PrettyTable(['Package', 'Version', 'Location', 'Status'])
        # Set each column as left "l" justified
        t.align['Package'] = t.align['Version'] = t.align['Location'] = \
            t.align['Status'] = "l"

        cmd_output = cmd(['pip list --format json -v'])

        # Pip list on RH/CEL can give lots of extra data when the -v
        # argument is used, so extract the list [...] of pip packages only
        extracted_json = re.match(r'.*(\[[\s\S]+\]).*', cmd_output)

        if extracted_json:
            data = json.loads(extracted_json.groups()[0])
            for pkg in data:
                if pkg['name'] in sucessful_package_list:
                    t.add_row([pkg['name'], pkg['version'], pkg['location'], 
                        Palette.paint("SUCCESS", FgColour.GREEN)])
                elif pkg['name'] in failed_package_list:
                    t.add_row([pkg['name'], pkg['version'], pkg['location'], 
                        Palette.paint("FAILURE", FgColour.RED, Style.BOLD)])
            log.info(str(t))

        if len(failed_package_list):
            log.error("Please refer to above log for error details of failures")

    def show_outdated_dev_mode_packages(self):
        cmd_output = cmd('pip list --outdated -e')
        
        # If pip is outdated, it will give a warning. If cmd_output starts with
        # this warning, then no packages are out of date
        if str(cmd_output).startswith("WARNING: You are using pip version"):
            log.error(str(cmd_output))
            return

        # At least one package is out of date
        if cmd_output != '':
            log.error(
                "\nThe following development mode packages are outdated. \nPull"
                " the latest code from git and if applicable, merge it into "
                "your branch. \n\n%s" % str(cmd_output))

    def run(self, args):
        log.info("\n" + banner("pyATS development mode tool"))
        packages = args.packages

        # Check for internal installation 
        ws_pkg_names = [p.project_name for p in working_set]
        if not args.external and self.is_internal_installation(ws_pkg_names):                   
            internal_installation = True
            log.info("Installation mode: Internal")
        else:
            internal_installation = False
            log.info("Installation mode: External")
      
        # If internal installation, load internal package metadata
        # If external installation, exclude internal pkgs 
        self.pkg_data = \
            self.rebuild_pkg_data(self.pkg_data, internal_installation)

        # Make sure that package names are correct and internal packages aren't 
        # being requested for an external pyats installation
        self.check_requested_packages_validity(packages, self.pkg_data)

        # Expand requested packages list if 'all' or 'genie.libs' in CLI list
        packages = self.rebuild_package_list(packages, self.pkg_data)

        # Check for potential pyATS version mismatch
        if not args.skip_version_check:
            self.check_version()

        # If user specifies a directory, then make it (if it doesn't exist)
        if args.directory:
            directory = self.create_directory(args.directory)
        else:
            directory = os.path.join(sys.prefix, 'pypi')
        log.debug("Repo Directory: %s" % directory)

        # Update/install latest pip and setuptools
        self.install_upgrade_pip_setuptools()

        # Loop through packages. Use a while loop as it allows for package list
        # to be manipulated during execution if needed
        successful_pkgs = []
        failed_pkgs = []
        while len(packages):
            pkg = packages[0]
            log.info(
                "Working on putting %s package into development mode..." % pkg)

            repo_name = self.pkg_data[pkg]['repo_name']

            # Rename repo directory if external to allow internal/external repos 
            # to coexist
            if not internal_installation:
                repo_name = 'ext_%s' % repo_name

            repo_dir = os.path.join(directory, repo_name)

            # If package is already in dev mode, then skip running make develop 
            # unless forced. If only cloning or if deleting the repo, don't skip
            if self.package_is_in_dev_mode(pkg) \
                    and not args.force_develop \
                    and not args.clone_only \
                    and not args.delete_repos:
                log.warning("Skipping %s package as it is already in "
                            "development mode\n" % pkg)
                packages.remove(pkg)
                continue

            # Put crucial parts into a while loop in case user tries to ctrl-c
            make_develop_finished = False
            while not make_develop_finished:
                try:
                    self.prepare_repo(pkg, self.pkg_data, repo_dir, 
                                      args.delete_repos)

                    # Make sure it's actually a git repo
                    self.check_git_repo_validity(repo_dir)
                    
                    # Don't run 'make develop' if --clone-only flag is set
                    if args.clone_only:
                        packages.remove(pkg)
                        break
                    
                    self.run_make_develop(pkg, repo_dir)

                except KeyboardInterrupt:
                    # User has pressed ctrl-c but exiting during this process 
                    # will likely result in a corrupted pyATS installation.
                    # So catch the first interrupt and wait. User can ctrl-c
                    # again to quit, otherwise restart step to repair package
                    self.show_keyboard_interrupt_warning_and_wait(
                        self.KEYBOARD_INTERRUPT_WAIT_TIME)

                    # Due to multiple genielibs packages being in the same repo,
                    # special handling is required after a keyboard interrupt. 
                    # Reinsert previous genielib packages. Remark the directory 
                    # for deletion if requested
                    if self.is_pkg_part_of_genielibs(pkg):
                        packages, successful_pkgs = \
                            self.reinsert_genielibs_pkgs(pkg, packages, 
                                                         successful_pkgs)
                        if args.delete_repos:
                            self.GENIELIBS_FLAGS['dir_deleted'] = False
                        self.GENIELIBS_FLAGS['repo_cloned'] = False
                        break
                    continue

                except Exception:
                    log.exception(
                        "\nThe following error occurred while trying to put the"
                        " %s package into development mode.\n" % pkg)
                    failed_pkgs.append(pkg)
                    packages.remove(pkg)
                    make_develop_finished = True
                    log.info("\n%s has not been put into development mode\n" 
                             % pkg)
                else:
                    # Log success message, add package to list of successfully 
                    # installed packages, and exit installation loop
                    log.info("\n%s has been put into development mode\n" % pkg)
                    successful_pkgs.append(pkg)
                    packages.remove(pkg)
                    make_develop_finished = True

        # Show pretty results
        log.info(banner("pyATS development mode tool results"))
        log.info("This tool's execution has put the following packages into "
                 "development mode:\n")
        self.show_results(successful_pkgs, failed_pkgs)
        self.show_outdated_dev_mode_packages()
