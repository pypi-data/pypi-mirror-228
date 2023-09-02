'''
This file has a large test file that takes a long time to run. 
(tests/large_tests/develop_undevelop_test.py)
So, it is not included in the standard "make test" command.
To test this file (and develop.py), run "make largetest". 
'''

# Import Python packages
import logging
from pathlib import Path
from pkg_resources import working_set

# Import pyATS packages
from pyats.cli.utils import cmd
from pyats.log.utils import banner

# Import local directory packages
from .develop import DevelopCommand

# Set up internal logger
log = logging.getLogger(__name__)


class UndevelopCommand(DevelopCommand):
    '''
    Command to remove pyATS packages from development mode
    '''

    name = 'undevelop'
    help = ('Removes desired pyATS packages from development mode ')
    description = '''
Removes listed pyATS packages from development mode. Each listed package is 
removed from development mode with 'make undevelop' and then is reinstalled 
using 'pip install <package>'. Internal Cisco packages will be reinstalled if 
the pyATS installation is internal, otherwise external packages will be 
reinstalled instead.'''

    usage = '''pyats undevelop [packages...] [options]
  
Usage Examples:
  pyats undevelop all
  pyats undevelop genie.libs.sdk --skip-version-check
  pyats undevelop genie.libs.parser genie.trafficgen --external
  pyats undevelop genie.libs unicon.plugins'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.parser.add_argument(
            "packages",
            type=str,
            nargs="*",
            help="Packages to remove from development mode. Available choices:"
                 "\nall, {}".format(", ".join(self.pkg_data.keys())))                                 
                        
        self.parser.add_argument(
            "-s", "--skip-version-check",
            action="store_true",
            help="Do not check if pyATS packages are up to date before tool "
                 "execution. WARNING: Using this option may lead to pyATS "
                 "package version conflicts which could result in a corrupted "
                 "pyATS installation! Use with discretion (Optional)")

        self.parser.add_argument(
            '-e', '--external',
            action='store_true',
            help="Reinstall external public pip packages instead of internal. "
                 "Only applicable to internal Cisco pyATS installations. "
                 "For external pyATS Installations, external public "
                 "pip packages will always be used (Optional)")


    def get_package_makefile_directory(self, package_name):   
        """ Uses pip to locate package directory. Returns Makefile location """
        
        # package_name can be pyats for internal installations only and internal
        # installations have ats packages only
        if package_name == 'pyats':
            package_name = 'ats' 

        for pkg in working_set:
            if pkg.project_name == package_name:
                makefile_dir = Path(pkg.location).parent

                if package_name == 'ats' \
                        or self.is_pkg_part_of_genielibs(package_name):
                    makefile_dir = Path(pkg.location).parents[2]
                
                log.debug("Makefile location: %s" % makefile_dir)
                return str(makefile_dir)

        raise Exception("Cannot find Makefile for %s package")

    def run_make_undevelop(self, pkg):
        log.info("Running 'make undevelop' for %s" % pkg)

        # Find package makefile location and set make target
        makefile_dir = self.get_package_makefile_directory(pkg)
        makefile_target = 'undevelop'

        # Use the custom make target for genie.libs packages to allow for
        # packages to be put into development mode individually
        if self.is_pkg_part_of_genielibs(pkg):
            package_name = pkg.split('.')[-1]
            makefile_target = 'undevelop-' + package_name

        try:
            cmd("make %s -C %s" % (makefile_target, makefile_dir))
        except Exception:
            log.exception(
                "\nAn error occurred during 'make undevelop' command for %s.\n"
                "It's possible that this error has corrupted your pyATS "
                "installation!\nIf necessary, please clone the %s repo and run "
                "'make develop' within the repo directory to manually repair.\n"
                % (pkg, pkg))
            raise
        else:
            log.debug(
                "'make undevelop' for %s package completed successfully" % pkg)

    def reinstall_pip_package(self, pkg, internal_installation):
        """ Reinstalls specified pip package (internal or external) """

        packages_to_reinstall = [pkg]
        if pkg == 'pyats': 
            packages_to_reinstall = self.pkg_data[pkg]['related_pkgs']

        for package in packages_to_reinstall:
            log.info("Reinstalling %s..." % package)

            try: 
                if internal_installation:
                    cmd("pip install --index-url "
                        "https://pyats-pypi.cisco.com/simple %s" % package)
                else:
                    cmd("pip install %s" % package)
            except Exception:
                log.exception(
                    "\nAn error occured during pip installation of %s package."
                    "\nIt's possible that this error has corrupted your pyATS "
                    "installation!\nIf necessary, then please use pip to "
                    "manually reinstall the %s package.\n" % (pkg, package))
                raise

    def run(self, args):
        log.info("\n" + banner("pyATS un-development mode tool"))
        packages = args.packages

        # Check for internal installation and rebuild pkg_data dict if needed
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

        # Update/install latest pip and setuptools
        self.install_upgrade_pip_setuptools()

        # Loop though packages supplied from CLI and record successes
        successful_pkgs = []
        failed_pkgs = []
        for pkg in packages:
            log.info(
                "Working on removing %s package from development mode..." % pkg)

            # If package is not in dev mode, skip package
            if not self.package_is_in_dev_mode(pkg):
                log.warn("Package %s is not in development mode.\n" % pkg)
                continue

            # Put crucial parts into a while loop in case user tries to ctrl-c
            make_undevelop_finished = False
            while not make_undevelop_finished:
                try:
                    self.run_make_undevelop(pkg)
                    self.reinstall_pip_package(pkg, internal_installation)
                except KeyboardInterrupt:
                    # Catch user if they try to quit at a bad time! 
                    # Ctrl-C again during this 5 second window, will exit
                    self.show_keyboard_interrupt_warning_and_wait(
                        self.KEYBOARD_INTERRUPT_WAIT_TIME)
                    continue
                except Exception:
                    log.exception(
                        "\nThe following error occurred while trying to remove "
                        "the %s package from development mode.\n" % pkg)
                    failed_pkgs.append(pkg)
                    packages.remove(pkg)
                    make_undevelop_finished = True
                    log.info("\n%s has not been removed from development mode\n" 
                             % pkg)
                else:
                    # Log success message, add package to list of successfully 
                    # installed packages, and exit reinstallation loop
                    log.info(
                        "\n%s has been removed from development mode. "
                        "Related packages have been reinstalled\n" 
                        % pkg)
                    successful_pkgs.append(pkg)
                    make_undevelop_finished = True

        # Show pretty results
        log.info(banner("pyATS un-development mode tool results"))
        log.info("This tool's execution has removed the following packages from"
                 " development mode:\n")
        self.show_results(successful_pkgs, failed_pkgs)
