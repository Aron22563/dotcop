import os
from pathlib import Path
from dotcop.utils.logging_setup import Logger
from dotcop.config.ConfigHandler import load_dotcop_config
from dotcop.config.ConfigHandler import load_dotcop_database

logger = Logger.get_logger(__name__)

class InstallCommand:
    def _install_package(self, package):
        self._query_remote(package)
        #self._test_local_package_paths(package)
        #self._test_local_package(package)
        #self._pull_remote(package)
        #self._finalize_install(package)
        #self._update_package_db(package)

    def _query_remote(self, package):
        self.package_metadata = "placeholder_metadata"
        #self.package_metadata = requests.head(f'https://dotcop.example.com/api/packages/{package}')
        print(self.package_metadata)

    def _test_local_package_paths(self, package):
        package_folder = Path(self.package_metadata['folder'])
        package_path = os.path.expandvars(self.configuration_file['package_path'])/package_folder
        if package_path.is_dir():
            logger.warn("This package is already installed, please remove it before reinstalling.")
            return
        package_path.mkdir(parents=True, exist_ok=False)

    def run(self, args):
        self.configuration_file = load_dotcop_config()
        self.database_file = load_dotcop_database()
        for package in args.packages:
            self._install_package(package)
