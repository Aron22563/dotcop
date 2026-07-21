class UnexpectedArgumentCount(Exception):
    def __init__(self, expected_argument_count, received_argument_count):
        self.expected_argument_count = expected_argument_count
        self.received_argument_count = received_argument_count
