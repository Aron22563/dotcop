from argparse import Namespace

from dotcop.utils.logging_setup import Logger
from dotcop.core.cli.exceptions.UnexpectedArgumentCount import UnexpectedArgumentCount

logger = Logger.get_logger(__name__)

def adapt_status_command(args):
    """
    @param args contains a list of all possible flags toggled as true or false.
    """
    if args.inactive:
        query = 'inactive'
    elif args.active:
        query = 'active'
    elif args.all:
        query = 'all'
    else:
        query = 'default_query'
    adapted_status_args = Namespace(query=query)
    print(adapted_status_args)
    return adapted_status_args

EXPECTED_ARGUMENT_COUNT = 1
def validate_status_args(args):
    """
    Tests whether args contains 0 or the expected amount of true flags.
    @param args contains a "mutually exclusive" (validated) list of possible flags.
    """
    dict_args = vars(args)
    true_argument_count = 0     
    for key in dict_args:
        if dict_args[key]: 
            true_argument_count+=1
    # Assume default value if no values are found true.
    if true_argument_count == 0: 
        true_argument_count +=1

    if true_argument_count != EXPECTED_ARGUMENT_COUNT: 
        raise UnexpectedArgumentCount(true_argument_count, EXPECTED_ARGUMENT_COUNT)
