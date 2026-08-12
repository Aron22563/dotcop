import yaml

from dotcop.config.ConfigHandler import load_database_file
from dotcop.data.ConfigFileDAL import ConfigFileDAL
from dotcop.utils.logging_setup import Logger
from dotcop.utils.formatter import Formatter
from dotcop.utils.exceptions.PackageFormatInvalid import PackageFormatInvalid
from dotcop.utils.exceptions.PackageMetadataInvalid import PackageMetadataInvalid
from dotcop.utils.exceptions.PackageStatusInvalid import PackageStatusInvalid
from dotcop.data.exceptions.DatabaseKeyMissing import DatabaseKeyMissing
from dotcop.data.exceptions.PackageNotFound import PackageNotFound

class PackageDatabaseDAL():
    def __init__(self):
        self.logger = Logger.get_logger(__name__)

    def get_packages_dict(self):
            all_packages = self._get_value_by_key('packages')
            return all_packages

    def get_packages_by_status(self, status): 
        all_packages = self.get_packages_dict()
        selected_packages = dict()
        for name, metadata in all_packages.items():
            try: 
                self._validate_package_metadata(metadata)
            except PackageMetadataInvalid:
                self.logger.error("Package status query failed because invalid metadata was found. This might be an unrelated malformed package")
                raise
            if metadata['status'] == status: 
                selected_packages[name] = metadata
        return selected_packages

    def get_package_metadata(self, package_name):
        """
        Retrieves a package, validates package_name, returns its associated metadata
        @Throws dotcop.data.exceptions.PackageNotFound
        @Throws dotcop.utils.exceptions.PackageFormatInvalid
        """
        try:
            self._validate_package_name(package_name)
        except PackageFormatInvalid:
            self.logger.error("Package metadata retrieval failed because of invalid name format")
            raise
        all_packages = self.get_packages_dict()
        try:
            package_metadata = all_packages[package_name]
        except KeyError:
            self.logger.error("Package not found: %s", package_name)
            raise PackageNotFound(package_name)
        return  package_metadata

    def update_package_status(self, package_name, status):
        try:
            self._validate_package_status(status)
        except PackageStatusInvalid:
            self.logger.error("Package status update failed because of invalid status")
            raise
        try:
            package_metadata = self.get_package_metadata(package_name)
        except (PackageFormatInvalid, PackageNotFound):
            self.logger.error("Package format invalid or not found")
            raise

        package_metadata['status'] = status
        self._update_package_metadata(package_name, package_metadata)

    def _get_value_by_key(self, key):
        database_file = self._load_database_file()
        try:
            value = database_file[key]
        except KeyError:
            exception_message = "Key was not found in database file"
            self.logger.error(exception_message)
            raise DatabaseKeyMissing(key, exception_message)
        return value

    def _update_package_metadata(self, package_name, package_metadata):
        # Throws PackageFormatInvalid
        try:
            self._validate_package_name(package_name)
        except PackageFormatInvalid:
            self.logger.error("Package metadata update failed because of invalid package name format")
            raise
        # Throws PackageMetadataInvalid
        try:
            self._validate_package_metadata(package_metadata)
        except PackageMetadataInvalid:
            self.logger.error("Package metadata update failed because of invalid metadata format")
            raise

        database_file = self._load_database_file()
        try:
            database_file["packages"]
        except KeyError:
            exception_message = "Missing \'packages\' key"
            self.logger.error(exception_message)
            raise DatabaseKeyMissing('packages', exception_message)
        try:
            database_file["packages"][package_name]
        except KeyError:
            self.logger.error("Package not found: %s", package_name)
            raise PackageNotFound(package_name)
        database_file["packages"][package_name] = package_metadata
        database_path = self._load_database_path()
        try:
            with open(database_path, "w") as f:
                yaml.safe_dump(database_file, f, sort_keys=False)
        except Exception:
            self.logger.error("Database package update failed for: %s", package_name)
            raise

    def _load_database_path(self):
            return ConfigFileDAL().get_database_path()

    def _load_database_file(self):
        database_path = self._load_database_path()
        database_file = load_database_file(database_path)
        return database_file

    def _validate_package_name(self, package_name):
        try:
            Formatter().check_pkgformat(package_name)
        except PackageFormatInvalid:
            raise

    def _validate_package_metadata(self, package_metadata):
        try:
            Formatter().check_package_metadata(package_metadata)
        except PackageMetadataInvalid:
            raise

    def _validate_package_status(self, package_status): 
        try: 
            Formatter().check_package_status(package_status)
        except PackageStatusInvalid: 
            raise


