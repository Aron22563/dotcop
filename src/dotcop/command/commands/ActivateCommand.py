
from dotcop.utils.logging_setup import Logger
from dotcop.core.Linker import Linker
from dotcop.data.PackageDatabaseDAL import PackageDatabaseDAL
from dotcop.data.MetaDirDAL import MetaDirDAL
from dotcop.data.exceptions.PackageNotFound import PackageNotFound
from dotcop.data.exceptions.LinkDestinationExists import LinkDestinationExists
from dotcop.data.exceptions.LinkSourceNotFound import LinkSourceNotFound
from dotcop.utils.exceptions.PackageFormatInvalid import PackageFormatInvalid
from dotcop.utils.exceptions.PackageDBMetadataInvalid import PackageDBMetadataInvalid
from dotcop.command.exceptions.PackageAlreadyActive import PackageAlreadyActive

class ActivateCommand:
    def __init__(self):
        self.logger = Logger.get_logger(__name__)

    def run(self, args):
        for package_name in args.packages:
            self.logger.info("Activating: %s", package_name)
            try: 
                self._activate_package(package_name)
            except Exception: 
                self.logger.error("Package activation aborted for: %s", package_name)

    def _activate_package(self, package_name):
        try:
            self.package_status = PackageDatabaseDAL().get_package_status(package_name)
        except PackageFormatInvalid:
            self.logger.error("Package activation failed because of an invalid package name format")
            raise
        except PackageNotFound: 
            self.logger.error("Package activation failed because the package was not found")
            raise
        except PackageDBMetadataInvalid: 
            self.logger.error("Package activation failed because the package db metadata was invalid")
            raise
        if self.package_status == 'active':
            self.logger.error("Package activation failed because the package is already active.")
            raise PackageAlreadyActive(package_name)

        try: 
            file_paths = self._load_file_paths(package_name)
        except LinkDestinationExists as e: 
            self.logger.error("Package activation failed because the destination files of a pair in the files list already exists: %s", e.dst_path)
            raise
        except SourceFileNotFound as e: 
            self.logger.error("Package activation failed because the source file of a pair in the files list was not found: %s", e.src_path)
            raise
        self._link_files(file_paths, package_name)
        self._update_package_db(package_name)

    def _load_file_paths(self, package_name):
        files_dict = MetaDirDAL().get_package_files_dict(package_name)
        return files_dict

    def _link_files(self, files_dict, package_name):
        linker = Linker(package_name)
        self.logger.info("Linking files for package: %s", package_name)
        for src_path, dst_path in files_dict.items():
            self.logger.info("%s -> %s", src_path, dst_path)
            linker.link(src_path, dst_path)

    def _update_package_db(self, package_name):
        PackageDatabaseDAL().update_package_status(package_name, 'active')
        self.logger.info("Package activated successfully: %s", package_name)
