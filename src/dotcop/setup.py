import argparse
from dotcop.utils.logging_setup import Logger
from dotcop.config import Config
from dotcop.parser import Parser
def main():
    cfg = Config()
    prs = Parser()
    config_file = cfg.load_configfile()
    args = prs.parse_arguments()
    print(args)

