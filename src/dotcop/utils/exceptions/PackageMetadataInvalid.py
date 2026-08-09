class PackageMetadataInvalid(Exception):
    def __init__(self, package_name, package_metadata, message):
        self.package_name = package_name
        self.package_metadata = package_metadata
        self.message = message
