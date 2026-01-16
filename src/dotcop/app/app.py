from dotcop.handlers.config_handler import ConfigHandler
from dotcop.handlers.command_handler import CommandHandler


class App:
    def __init__(self):
        self.config_handler = ConfigHandler()
        self.command_handler = CommandHandler()

    def run(self):
        config = self.config_handler.load_dotcop_config()

        args = self.command_handler.run()
