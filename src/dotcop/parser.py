import argparse 
import pathlib
from dotcop.utils.logging_setup import Logger
from dotcop.utils.formatter import Formatter

class Parser: 
    def __init__(self): 
        self.logger = Logger.get_logger(__name__)
        self.init_parser()
        self.sub_parser()
    def check_pkgformat(self, args): 
            formatter = Formatter()
            valid_packages = [pkg for pkg in args.packages if formatter.check_pkgformat(pkg)]

            invalid_packages = set(args.packages) - set(valid_packages) 
            if(valid_packages == []):
                self.logger.critical(f"Package names follow: @user/pkgname:version with a Semantic Versioning version string. Invalid packages: {', '.join(invalid_packages)}")
                raise RuntimeError
            args.packages = valid_packages

    def parse_arguments(self): 
        try:    
            args = self.parser.parse_args()
            self.logger.debug(f"Arguments parsed as: {args}")
            if hasattr(args, "packages"):
                self.check_pkgformat(args)
            return args
        except Exception as e: 
            raise

    def init_parser(self): 
        self.parser = argparse.ArgumentParser(
            prog="Dotcop",
            description="Configuration package manager for versioning and synchronization of Linux configuration files.",
            epilog="This is currently a work in progress, use with caution..."
        )

    def sub_parser(self):
        subparsers = self.parser.add_subparsers(dest="command", required=True)

        subparsers.add_parser("help", help="Show help message")
        subparsers.add_parser("status", help="Show status")
        subparsers.add_parser("list", help="List installed configurations")
        subparsers.add_parser("create", help="Create a new program configuration")
        subparsers.add_parser("edit", help="Edit an existing program configuration")

        install_parser = subparsers.add_parser(
                "install",
                help="Install a configuration",
                description="Install a configuration package into the system."
        )
        install_parser.add_argument("packages", nargs="+", help="Package name to install")
        install_parser.add_argument("--force", action="store_true", default=False,  help="Force installation")
        
        remove_parser = subparsers.add_parser(
                "remove",
                help="Remove a configuration",
                description="Remove a configuration package from the system"
        )
        remove_parser.add_argument("packages", nargs="+", help="Package name to remove")
        remove_parser.add_argument("--force", action="store_true", default=False, help="Force removal")


