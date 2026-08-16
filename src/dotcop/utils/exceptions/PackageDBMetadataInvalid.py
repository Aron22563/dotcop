class PackageDBMetadataInvalid(Exception):
    def __init__(self, package_metadata, message):
        self.package_metadata = package_metadata
        self.message = message
