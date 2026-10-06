from dotcop.utils.logging_setup import Logger
from dotcop.data.PackageDatabaseDAL import PackageDatabaseDAL

class StatusCommand:
    def __init__(self):
        self.logger = Logger.get_logger(__name__)

    def _get_packages_by_query(self, query):
        selected_packages = set()
        match query:
            case 'all':
                selected_packages = set(PackageDatabaseDAL().get_packages_dict().keys())
            case 'active':
                selected_packages = set(PackageDatabaseDAL().get_packages_by_status(query).keys())
            case 'inactive':
                selected_packages = set(PackageDatabaseDAL().get_packages_by_status(query).keys())
            case 'default_query':
                selected_packages = set(PackageDatabaseDAL().get_packages_dict().keys())
        return selected_packages

    def run(self, query):
        self.logger.info("StatusCommand executing with: %s", query)
        selected_packages = self._get_packages_by_query(query)
        for pkgname in sorted(selected_packages):
            print(pkgname)
