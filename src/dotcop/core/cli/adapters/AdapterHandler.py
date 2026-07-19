from argparse import Namespace

from dotcop.utils.logging_setup import Logger
from dotcop.core.cli.adapters.status_adapter import adapt_status_command
from dotcop.core.cli.adapters.status_adapter import validate_status_args

logger = Logger.get_logger(__name__)

# This translates raw cli flags into domain objects. It decouples the cli from the execution layer.
class AdapterHandler:
    def run(self, args):
        adapted_args = args
        command = args.command

        # Pass only flags to dedicated command adapters.
        cleaned_args = args
        del cleaned_args.command
        match command: 
            case 'status':
                validate_status_args(cleaned_args)
                adapted_args = adapt_status_command(cleaned_args)
        adapted_args = Namespace(command=command, query=adapted_args.query)
        logger.debug("Adapted args: %s", adapted_args)
        return adapted_args

