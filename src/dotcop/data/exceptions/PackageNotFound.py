class PackageNotFound(Exception):
    def __init__(self, package_name):
        self.package_name = package_name
