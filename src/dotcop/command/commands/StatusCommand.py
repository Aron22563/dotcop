
from dotcop.utils.logging_setup import Logger
from dotcop.config.ConfigHandler import load_dotcop_database

class StatusCommand:
    def __init__(self):
        self.logger = Logger.get_logger(__name__)
    def _evaluate_cli_args_to_status(self, args):
        if args.inactive:
             return 'inactive'
        if args.active:
            return 'active'
        return 'all'

    def _group_packages_by_status(self, packages, status):
        selected_packages = set()
        if status == 'all': 
            print("This should print all packages regardless of status flag")
            selected_packages = set(packages.keys())
        for name, metadata in packages.items():
            if metadata['status'] == status:
                selected_packages.add(name)
        return selected_packages

    def run(self, args):
        database_file = load_dotcop_database()
        args_status = self._evaluate_cli_args_to_status(args)
        selected_packages = self._group_packages_by_status(database_file['packages'], args_status)
        for package in selected_packages:
            print(package)
        self.logger.info("Database file was loaded by StatusCommand")
