from argparse import Namespace

from dotcop.utils.logging_setup import Logger

logger = Logger.get_logger(__name__)

def adapt_status_command(args):
    if args.inactive:
        query = 'inactive'
    elif args.active:
        query = 'active'
    elif args.all:
        query = 'all'
    adapted_status_args = Namespace(command=args.command, query=query)
    return adapted_status_args
