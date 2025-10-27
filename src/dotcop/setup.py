from dotcop.config import Config
from dotcop.parser import Parser


def main():
    cfg = Config()
    prs = Parser()
    config_file = cfg.load_configfile()
    print(config_file)
    try:
        args = prs.parse_arguments()
    except RuntimeError:
        print("Critical error occured during argument parsing")

        # Build cleaner process management/ exit system
        exit(1)
    print(args)
