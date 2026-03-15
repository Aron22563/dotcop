from dotcop.utils.logging_setup import Logger

from dotcop.core.cli.adapters.status_adapter import adapt_status_command

logger = Logger.get_logger(__name__)

# This translates raw cli flags into domain objects. It decouples the cli from the execution layer.
class AdapterHandler:
    def run(self, args):
        adapted_args = args
        if(args.command == 'status'): 
            adapted_args = adapt_status_command(args)
        
        logger.debug("Adapted args: %s", adapted_args)
        return adapted_args
    
    
