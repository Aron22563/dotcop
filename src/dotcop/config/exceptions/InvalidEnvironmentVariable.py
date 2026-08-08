class InvalidEnvironmentVariable(Exception):
    def __init__(self, variable_name):
        self.variable_name = variable_name
