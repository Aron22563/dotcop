class PackageFormatInvalid(Exception):
    def __init__(sel, package_name, message):
        self.package_name = package_name
        self.message = message
