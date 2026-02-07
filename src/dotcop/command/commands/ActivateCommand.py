import os
import yaml
from pathlib import Path
from yaml import YAMLError

from dotcop.utils.logging_setup import Logger
from dotcop.config.ConfigHandler import load_dotcop_config
from dotcop.config.ConfigHandler import load_dotcop_database
from dotcop.core.Linker import Linker

logger = Logger.get_logger(__name__)

class ActivateCommand:
     def run(self, args): 
        self.configuration_file = load_dotcop_config()
        self.database_file = load_dotcop_database()
        for package in args.packages: 
            src_path, dst_path = self._test_package(package)
            print(f"{src_path} -> {dst_path}")

        for package in args.packages: 
            self._load_package(src_path, dst_path)
            
    def _test_package(self, package):
        self._load_db_metadata(package)
        self._test_package_setup(package)
        src_path, dst_path = self._test_file_paths(package)
        return src_path, dst_path

    def _load_db_metadata(self, package):
        logger.info(f"Activating: {package}")
        package_name = package
        self.package_metadata = self.database_file['packages'].get(package_name)
        if self.package_metadata['active'] == True:
            logger.error("Package is already active, exiting")
            return
    
    def _test_package_setup(self, package):
        package_folder = Path(self.package_metadata['folder'])
        self.package_path = Path(os.path.expandvars(self.configuration_file['package_path'])) / package_folder
        if not self.package_path.is_dir(): 
            logger.error(f"Package was not found at expected path: {self.package_path}")
            return

        metadata_file_path = self.package_path / "metadata.yaml" 
        if not metadata_file_path.is_file(): 
            logger.error(f"Metadata file not found in folder: {metadata_file_path}")
            return 
        try:
            with open(metadata_file_path, "r") as file:
                self.metadata_file = yaml.safe_load(file)
        except YAMLError as e:
            logger.critical(f"Failed to parse metadata file at: {metadata_file_path}")
            raise 

        self.files_folder_path = self.package_path / "files"
        if not self.files_folder_path.is_dir():
            logger.error(f"Files folder not found in: {self.files_folder_path}")
            return 

    def _test_file_paths(self, package): 
        for pair in self.metadata_file["files"]: 
            src = pair["from"]
            dst = pair["to"]
            src_path = self.package_path /"files"/ src
            if not src_path.is_file(): 
                logger.error(f"File not found: {src_path}")
                return
            dst_path = Path(os.path.expandvars(dst))
            if dst_path.is_file(): 
                logger.error(f"Existing file found: {dst_path}")
                return
            return src_path, dst_path

    def _load_package(self, src_path, dst_path):
        package_folder = Path(self.package_metadata['folder'])
        linker = Linker(package_folder)
        self._load_files(linker, src_path, dst_path)
        #self._finalize_install(package)
        self._update_package_db()

    def _load_files(self, linker, src_path, dst_path): 
        linker.link(src_path, dst_path)

    def _update_package_db(self):
        self.package_metadata['active'] = True