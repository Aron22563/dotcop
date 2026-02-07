
from dotcop.utils.logging_setup import Logger
from dotcop.config.ConfigHandler import load_dotcop_database

class StatusCommand:
    def __init__(self):
        self.logger = Logger.get_logger(__name__)

    def _group_packages(self, packages):
        active_packages = set()
        inactive_packages = set()

        for name, metadata in packages.items():
            if metadata['active']:
                active_packages.add(name)
            else:
                inactive_packages.add(name)
        return active_packages, inactive_packages

    def run(self, args):
        database_file = load_dotcop_database()
        active_packages, inactive_packages = self._group_packages(database_file['packages'])
        for package in active_packages:
            print(package)
        self.logger.info("Database file was loaded by StatusCommand")
