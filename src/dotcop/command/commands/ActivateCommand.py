import os
import requests 
from pathlib import Path
from dotcop.utils.logging_setup import Logger
from dotcop.config.ConfigHandler import load_dotcop_config
from dotcop.config.ConfigHandler import load_dotcop_database

logger = Logger.get_logger(__name__)

class ActivateCommand:
    def _activate_package(self, package):
        self._load_db_metadata(package)
        self._test_package_setup(package)
        #self._test_file_paths(package)
        #self._load_files(package)
        #self._finalize_install(package)
        #self._update_package_db(package)
    def _load_db_metadata(self, package):
        logger.info(f"Activating: {package}")
        package_name = package
        self.package_metadata = self.database_file['packages'].get(package_name)
        if self.package_metadata['active'] == True:
            logger.error("Package is already active, exiting")
            return
    
    def _test_package_setup(self, package):
        package_folder = Path(self.package_metadata['folder'])
        package_path = Path(os.path.expandvars(self.configuration_file['package_path'])) / package_folder
        if not package_path.is_dir(): 
            logger.error(f"Package was not found at expected path: {package_path}")
            return

        metadata_file_path = package_path / "metadata.yaml" 
        if not metadata_file_path.is_file(): 
            logger.error(f"Metadata file not found in folder: {metadata_file_path}")
            return 

        files_folder_path = package_path / "files"
        if not files_folder_path.is_dir():
            logger.error(f"Files folder not found in: {files_folder_path}")
            return 
    
    def run(self, args): 
        self.configuration_file = load_dotcop_config()
        self.database_file = load_dotcop_database()
        for package in args.packages: 
            self._activate_package(package)