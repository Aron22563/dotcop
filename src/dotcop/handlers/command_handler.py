from dotcop.app.cli import Parser


class CommandHandler:
    def __init__(self):
        self.parser = Parser()

    def run(self):
        args = self.parser.parse_arguments()
        return args
