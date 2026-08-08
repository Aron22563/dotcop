from dotcop.config.ConfigHandler import load_database_file
from dotcop.data.ConfigFileDAL import ConfigFileDAL
from dotcop.utils.logging_setup import Logger

class PackageDatabaseDAL():
    def __init__(self): 
        self.logger = Logger.get_logger(__name__)

    def _load_database_file(self):
        database_path = ConfigFileDAL().get_database_path()
        database_file = load_database_file(database_path)
        return database_file

    def _get_value_by_key(self, key):
        database_file = self._load_database_file()
        value = database_file.get(key)
        if value:
            return value
        self.logger.error("Value was not found in database file: {}", key)
        raise KeyError
    
    def get_all_packages(self):
        all_packages = self._get_value_by_key('packages')
        return all_packages 
