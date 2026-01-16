from dotcop.config.ConfigHandler import ConfigHandler
from dotcop.command.CommandHandler import CommandHandler
from dotcop.core.cli import Parser


class App:
    def __init__(self):
        self.config_handler = ConfigHandler()
        self.command_handler = CommandHandler()
        self.parser = Parser()

    def run(self):
        config = self.config_handler.load_dotcop_config()
        args = self.parser.parse_arguments()
        self.command_handler.execute_action(args, config)
