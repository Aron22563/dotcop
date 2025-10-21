import semver

from parse import parse

class Formatter: 
    def __init__(self): 
        self.logger = Logger.get_logger(__name__)

    def check_version(self, version):
        if semver.Version.is_valid(version):
            return True
        else:
           return False



    # Validate whether a given package string follows the format "@user/pkgname:version", the version specification is optional, it should default to latest
    def check_pkgformat(self, pkg):
        # Parse pkgname with version string 
        result = parse("@{user}/{name}:{version}", pkg)
        if result is not None:
            # Test version string
            version = result["version"] or None
            if version and not self.check_version(version):
                self.logger.error(f"Invalid version format found in package name found: {pkg}")
                return False
            return True
        # Parse pkgname without version string
        result = parse("@{user}/{name}", pkg)
        if result is None:
            self.logger.error(f"Invalid package name format found: {pkg}")
            return False
        return True
