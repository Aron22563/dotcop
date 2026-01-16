import logging
logger = logging.getLogger(__name__)

from dotcop.core.cli import Parser
from dotcop.command.commands import HelpCommand, StatusCommand, ListCommand, CreateCommand, InstallCommand, RemoveCommand

class CommandHandler:
    def __init__(self):
        self.parser = Parser()

    def run(self, config):
        logger.warn("Configuration was ignored")
        args = self.parser.parse_arguments()
        return args

    def execute_action(self, args, config):
        command = args.command
        match command:
            case 'status': 
                logger.info("Status Command was called")
            case 'list': 
                logger.info("List Command was called")
            case 'create': 
                logger.info("Create Command was called")
            case 'edit': 
                logger.info("Edit Command was called")
            case 'install': 
                logger.info("Installation Command called")
            case 'remove': 
                logger.info("Remove Command was called")

        return None