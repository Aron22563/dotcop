class PackageFormatInvalid(Exception):
    def __init__(self, package_name, message):
        self.package_name = package_name
        self.message = message
