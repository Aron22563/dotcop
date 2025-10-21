import argparse
from dotcop.utils.logging_setup import Logger
from dotcop.config import Config
from dotcop.parser import Parser
def main():
    cfg = Config()
    prs = Parser()
    config_file = cfg.load_configfile()
    try: 
        args = prs.parse_arguments()
    except RuntimeError as e: 
        print(f"Critical error occured during argument parsing")

        # Build cleaner process management/ exit system
        exit(1)
    print(args)
