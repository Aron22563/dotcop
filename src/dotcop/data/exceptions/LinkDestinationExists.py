class LinkDestinationExists(Exception):
    def __init__(self, dst_path, message):
        self.dst_path = dst_path
        self.message = message
