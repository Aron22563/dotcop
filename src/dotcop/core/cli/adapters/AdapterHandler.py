from argparse import Namespace

from dotcop.utils.logging_setup import Logger
from dotcop.core.cli.adapters.status_adapter import adapt_status_command
from dotcop.core.cli.adapters.status_adapter import validate_maximum_argument_count

logger = Logger.get_logger(__name__)

# This translates raw cli flags into domain objects. It decouples the cli from the execution layer.
class AdapterHandler:
    def run(self, args):
        command = args.command
        adapted_args = args
        
        match command: 
            case 'status':
                validate_maximum_argument_count(vars(args))
                adapted_args = adapt_status_command(vars(args))
        logger.debug("Adapted args: %s", adapted_args)
        return adapted_args

