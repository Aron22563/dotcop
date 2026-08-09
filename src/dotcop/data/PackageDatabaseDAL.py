import yaml

from dotcop.config.ConfigHandler import load_database_file
from dotcop.data.ConfigFileDAL import ConfigFileDAL
from dotcop.utils.logging_setup import Logger
from dotcop.utils.formatter import Formatter
from dotcop.utils.exceptions.PackageFormatInvalid import PackageFormatInvalid
from dotcop.utils.exceptions.PackageMetadataInvalid import PackageMetadataInvalid
from dotcop.data.exceptions.DatabaseKeyMissing import DatabaseKeyMissing
from dotcop.data.exceptions.PackageNotFound import PackageNotFound

class PackageDatabaseDAL():
    def __init__(self):
        self.logger = Logger.get_logger(__name__)

    def get_packages_dict(self):
            all_packages = self._get_value_by_key('packages')
            return all_packages

    def get_package_metadata(self, package_name):
        """
        Retrieves a package, validates package_name, returns its associated metadata
        @Throws dotcop.data.exceptions.PackageNotFound
        @Throws dotcop.utils.exceptions.PackageFormatInvalid
        @Throws dotcop.utils.exceptions.PackageMetadataInvalid
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
            package_metadata = self.get_package_metadata(package_name)
            package_metadata['status'] = status
            self._update_package_metadata(package_name, package_metadata)

        except Exception:
            self.logger.error("Package status update to: %s failed for package: %s", status, package_name)
            raise

    def _get_value_by_key(self, key):
        database_file = self._load_database_file()
        value = database_file.get(key)
        if value:
            return value
        self.logger.error("Value was not found in database file: {}", key)
        raise KeyError

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

    def _validate_package_metadata(package_name, package_metadata):
        try:
            Formatter().check_package_metadata(package_metadata)
        except PackageMetadataInvalid:
            raise


