from dotcop.config.ConfigHandler import load_config_file
from dotcop.data.ConfigFileInterface import ConfigFileInterface 
from dotcop.utils.logging_setup import Logger

class ConfigFileDAL(ConfigFileInterface):
    def __init__(self):
        self.logger = Logger.get_logger(__name__) 
    
    def _load_config_file(self):
        config_file = load_config_file() 
        return config_file

    def _get_value_by_key(self, key):
        config_file = self._load_config_file() 
        value = config_file.get(key)
        if value: 
            return value
        logger.error("Value was not found in configuration file: {}", key)
        raise KeyError

    def get_name_field(self) -> str: 
        return self._get_value_by_key('name')

    def get_log_path(self) -> str: 
        return self._get_value_by_key('log_path')

    def get_package_path(self) -> str: 
        return self._get_value_by_key('package_path')
        
    def get_database_path(self) -> str: 
        return self._get_value_by_key('dotcop_database')

    def get_meta_path(self) -> str: 
        return self._get_value_by_key('dotcop_meta')
