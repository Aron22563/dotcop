from dotcop.utils.logging_setup import Logger

from dotcop.core.cli import Parser
from dotcop.command.commands.StatusCommand import StatusCommand
from dotcop.command.commands.ListCommand import ListCommand
from dotcop.command.commands.CreateCommand import CreateCommand
from dotcop.command.commands.InstallCommand import InstallCommand
from dotcop.command.commands.RemoveCommand import RemoveCommand

class CommandHandler:
    def __init__(self):
        self.logger = Logger.get_logger(__name__)
        self.status_command = StatusCommand()
        self.list_command = ListCommand() 
        self.create_command = CreateCommand() 
        self.install_command = InstallCommand()
        self.remove_command = RemoveCommand()

    def execute_action(self, args):
        command = args.command
        match command:
            case 'status': 
                self.logger.info("Status Command was called")
                self.status_command.run(args)
            case 'list': 
                self.logger.warn("List Command was called")
            case 'create': 
                self.logger.warn("Create Command was called")
            case 'edit': 
                self.logger.warn("Edit Command was called")
            case 'install': 
                self.logger.warn("Installation Command called")
            case 'remove': 
                self.logger.warn("Remove Command was called")