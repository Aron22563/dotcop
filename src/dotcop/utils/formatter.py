import semver
from parse import parse
from dotcop.utils.logging_setup import Logger
from dotcop.utils.exceptions.PackageFormatInvalid import PackageFormatInvalid
from dotcop.utils.exceptions.PackageMetadataInvalid import PackageMetadataInvalid
from dotcop.utils.exceptions.PackageStatusInvalid import PackageStatusInvalid

class Formatter:
    def __init__(self):
        self.logger = Logger.get_logger(__name__)

    def check_version(self, version):
        if semver.Version.is_valid(version):
            return True
        else:
            return False

    def check_pkgformat(self, pkg):
        """
        Validate whether a given package string follows the format "@user/pkgname:version".
        The version specification is optional, it should default to latest.
        """
        # Parse pkgname with version string
        result = parse("@{user}/{name}:{version}", pkg)
        if result is not None:
            # Test version string
            version = result["version"]
            if not self.check_version(version):
                self.logger.error(f"Invalid version format found in package name found: {pkg}")
                raise PackageFormatInvalid(pkg, "Invalid version format")
            return True
        # Parse pkgname without version string
        result = parse("@{user:w}/{name:w}", pkg)
        if result is None:
            self.logger.error(f"Invalid package name format found: {pkg}")
            raise PackageFormatInvalid(pkg, "Invalid name format")
        return True

    def check_package_metadata(self, package_metadata):
        """
        Validates whether all necessary keys exist, does not yet verify their values.
        """
        try:
            package_metadata['folder']
        except KeyError:
            exception_message = "Missing \'folder\' key"
            self.logger.error(exception_message)
            raise PackageMetadataInvalid(package_metadata, exception_message)
        try:
            package_metadata['source']
        except KeyError:
            exception_message = "Missing \'source\' key"
            self.logger.error(exception_message)
            raise PackageMetadataInvalid(package_metadata, exception_message)
        try:
            package_metadata['status']
        except KeyError:
            exception_message = "Missing \'status\' key"
            self.logger.error(exception_message)
            raise PackageMetadataInvalid(package_metadata, exception_message)

    def check_package_status(self, package_status):
        if package_status not in ['default_query', 'active', 'inactive', 'all']: 
            exception_message = "Invalid package status was found"
            self.logger.error(exception_message)
            raise PackageStatusInvalid(package_status, exception_message)

