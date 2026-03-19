from dotcop.core.cli.Parser import Parser
from dotcop.core.cli.adapters.AdapterHandler import AdapterHandler
from dotcop.command.CommandHandler import CommandHandler


class App:
    def __init__(self):
        self.parser = Parser()
        self.adapter_handler = AdapterHandler()
        self.command_handler = CommandHandler()

    def run(self):
        args = self.parser.parse_arguments()
        adapted_args = self.adapter_handler.run(args)
        self.command_handler.execute_action(adapted_args)
