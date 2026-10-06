class PackageStatusInvalid(Exception):
    def __init__(self, package_status, message):
        self.package_status = package_status
        self.message = message
