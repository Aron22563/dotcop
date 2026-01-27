from dotcop.command.CommandHandler import CommandHandler
from dotcop.core.cli import Parser


class App:
    def __init__(self):
        self.command_handler = CommandHandler()
        self.parser = Parser()

    def run(self):
        args = self.parser.parse_arguments()
        self.command_handler.execute_action(args)
