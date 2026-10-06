class PathExpansionFailure(Exception):
    def __init__(self, path, message):
        self.path = path
        self.message = message
