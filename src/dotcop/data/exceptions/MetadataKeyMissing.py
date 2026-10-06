class MetadataKeyMissing(Exception):
    def __init__(self, key, message):
        self.key = key
        self.message = message
