from argparse import Namespace

from dotcop.utils.logging_setup import Logger

logger = Logger.get_logger(__name__)

def adapt_status_command(args):
    if args.inactive == True: 
        query = 'inactive'
    elif args.active == True: 
        query = 'active' 
    elif args.all == True: 
        query = 'all' 
    adapted_status_args = Namespace(command=args.command, query=query)
    return adapted_status_args