class LinkSourceNotFound(Exception):
    def __init__(self, src_path, message):
        self.src_path = src_path
        self.message = message
