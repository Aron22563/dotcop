from dotcop.utils.logging_setup import Logger
from dotcop.config.ConfigHandler import load_dotcop_database

class StatusCommand:
    def __init__(self):
        self.logger = Logger.get_logger(__name__)

    def _group_packages_by_query(self, packages, query):
        selected_packages = set()
        if query == 'all':
            selected_packages = set(packages.keys())
        else:
            for name, metadata in packages.items():
                if metadata['status'] == query:
                    selected_packages.add(name)
        return selected_packages

    def run(self, query):
        database_file = load_dotcop_database()
        self.logger.debug("StatusCommand executed with: %s", query)
        selected_packages = self._group_packages_by_query(database_file['packages'], query)
        for package in sorted(selected_packages):
            print(package)
