import argparse
from dotcop.utils.logging_setup import Logger
from dotcop.config import Config
from dotcop.parser import Parser
def main():
    cfg = Config()
    config_file = cfg.load_configfile()

    # Initialize argument parsing
    parser = argparse.ArgumentParser(
        prog="Dotcop",
        description="Configuration package manager for versioning and synchronization of Linux configuration files.",
        epilog="This is currently a work in progress, use with caution..."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("help", help="Show help message")
    subparsers.add_parser("status", help="Show status")
    subparsers.add_parser("list", help="List installed configurations")

    install_parser = subparsers.add_parser("install", help="Install a configuration")
    install_parser.add_argument("package", help="Package name to install")
    install_parser.add_argument("--version", help="Specific version to install")
    install_parser.add_argument("--force", action="store_true", help="Force reinstall")
    
    remove_parser = subparsers.add_parser("remove", help="Remove a configuration")
    remove_parser.add_argument("package", help="Package name to remove")

    args = parser.parse_args()
    core=Core()
    if args.command == "help":
        parser.print_help()
    elif args.command == "status":
        core.status()
    elif args.command == "list":
        core.list()
    elif args.command == "install":
        core.install(package=args.package, version=args.version, force=args.force)
    elif args.command == "remove":
        core.remove(package=args.package)
    else:
        parser.print_help()

class Core:
    # Check update status, vulnerability issues, anything basically
    def status(self):
        pass
    # List installed packages
    def list(self):
        pass
    def install(self, package, version, force):
        print(package, version, force) 
    def remove(self, package): 
        print(package)
