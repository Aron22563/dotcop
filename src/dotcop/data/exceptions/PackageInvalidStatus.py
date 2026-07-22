class PackageInvalidStatus(Exception):
    def __init__(self, message, package_name):
        self.message = message
        self.package_name = package_name
