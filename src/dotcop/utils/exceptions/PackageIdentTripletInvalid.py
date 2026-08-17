class PackageIdentTripletInvalid(Exception):
    def __init__(self, ident_triplet, message):
        self.ident_triplet = ident_triplet
        self.message = message

    def set_package_name(self, package_name):
        self.package_name = package_name
