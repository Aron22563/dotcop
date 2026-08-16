
from dotcop.utils.logging_setup import Logger
from dotcop.core.Linker import Linker
from dotcop.data.PackageDatabaseDAL import PackageDatabaseDAL
from dotcop.data.MetaDirDAL import MetaDirDAL
from dotcop.data.exceptions.PackageDBMetadataInvalid import PackageDBMetadataInvalid
from dotcop.data.exceptions.PackageNotFound import PackageNotFound
from dotcop.data.exceptions.PackageFormatInvalid import PackageFormatInvalid
from dotcop.command.exceptions.PackageAlreadyActive import PackageAlreadyActive

class ActivateCommand:
    def __init__(self):
        self.logger = Logger.get_logger(__name__)

    def run(self, args):
        for package_name in args.packages:
            self.logger.info("Activating: %s", package_name)
            self.logger.info("Package status for: %s is %s", package_name, PackageDatabaseDAL().get_package_status(package_name))
            self._activate_package(package_name)

    def _activate_package(self, package_name):
        try:
            self.package_status = PackageDatabaseDAL().get_package_status(package_name)
        except (PackageFormatInvalid, PackageNotFound, PackageDBMetadataInvalid):
            self.logger.error("Package activation failed")
            raise
        if self.package_status == 'active':
            self.logger.error("Package activation failed because the package is already active.")
            raise PackageAlreadyActive(package_name)

        file_paths = self._load_file_paths(package_name)
        self._load_package(file_paths, package_name)

    def _load_file_paths(self, package_name):
        self.logger.info("file path load triggered")
        files_dict = MetaDirDAL().get_package_files_dict(package_name)
        print(files_dict)

    def _load_package(self, file_paths, package_name):
        linker = Linker(package_name)
        for src_path, dst_path in file_paths:
            self.logger.info(f"{src_path} -> {dst_path}")
            linker.link(src_path, dst_path)
        #self._finalize_install(package)
        self._update_package_db(package_name)

    def _update_package_db(self, package_name):
        #self.package_metadata['active'] = True
        #PackageDatabaseDAL().update_dotcop_database_package(package, self.package_metadata)
        self.logger.info(f"Package activated: {package_name}")
