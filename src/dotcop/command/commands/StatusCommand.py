from dotcop.utils.logging_setup import Logger
from dotcop.config.ConfigHandler import load_dotcop_database
from dotcop.data.PackageDatabaseDAL import PackageDatabaseDAL

class StatusCommand:
    def __init__(self):
        self.logger = Logger.get_logger(__name__)

    def _group_packages_by_query(self, packages, query):
        selected_packages = set()
        match query:
            case 'all':
                selected_packages = set(packages.keys())
            case 'active':
                selected_packages = self._group_packages_by_status(packages, query)
            case 'inactive':
                selected_packages = self._group_packages_by_status(packages, query)
            case 'default_query':
                selected_packages = set(packages.keys())
        return selected_packages

    def _group_packages_by_status(self, packages, query):
        """
        Returns a filtered set of packages by their status

        @param packages contains the dict of packages.
        @param query contains the status to filter by.
        """
        selected_packages = set()
        for name, metadata in packages.items():
            if metadata['status'] == query:
                selected_packages.add(name)
        return selected_packages

    def run(self, query):
        all_packages = PackageDatabaseDAL().get_all_packages()
        self.logger.info("StatusCommand executing with: %s", query)
        selected_packages = self._group_packages_by_query(all_packages, query)
        for package in sorted(selected_packages):
            print(package)
