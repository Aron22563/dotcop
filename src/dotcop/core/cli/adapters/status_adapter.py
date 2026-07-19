from argparse import Namespace

from dotcop.utils.logging_setup import Logger
from dotcop.core.cli.exceptions.UnexpectedArgumentCount import UnexpectedArgumentCount

logger = Logger.get_logger(__name__)

def adapt_status_command(args):
    """
    @param args contains a dict of all possible flags toggled true or false.
    """

    if args['inactive']:
        query = 'inactive'
    elif args['active']:
        query = 'active'
    elif args['all']:
        query = 'all'
    else:
        query = 'default_query'
    adapted_status_args = Namespace(command=args['command'], query=query)
    print(adapted_status_args)
    return adapted_status_args

MAX_ARGUMENT_COUNT = 1
def validate_maximum_argument_count(args):
    """
    Tests whether args contains 0 or the expected amount of true flags.
    @param args contains a "mutually exclusive" (asserted here) dict of possible flags.
    """
    
    true_argument_count = 0     
    for key in args:
        if key == 'command': 
            break
        if args[key]: 
            true_argument_count+=1

    if true_argument_count > MAX_ARGUMENT_COUNT: 
        raise UnexpectedArgumentCount(true_argument_count, MAX_ARGUMENT_COUNT)
