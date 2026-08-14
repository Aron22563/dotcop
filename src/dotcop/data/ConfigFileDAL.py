import os
from pathlib import Path

from dotcop.utils.logging_setup import Logger
from dotcop.config.ConfigHandler import load_config_file
from dotcop.data.exceptions.ConfigKeyMissing import ConfigKeyMissing

class ConfigFileDAL():
    def __init__(self):
        self.logger = Logger.get_logger(__name__)

    def get_name_field(self) -> str:
        name_field = self._get_value_by_key('name')
        return name_field

    def get_log_path(self) -> str:
        log_path = self._expand_path_from_string(self._get_value_by_key('log_path'))
        return log_path

    def get_package_path(self) -> Path:
        package_path = self._expand_path_from_string(self._get_value_by_key('package_path'))
        return package_path

    def get_database_path(self) -> Path:
        database_path = self._expand_path_from_string(self._get_value_by_key('dotcop_database'))
        return database_path

    def get_meta_path(self) -> Path:
        meta_path = self._expand_path_from_string(self._get_value_by_key('dotcop_meta'))
        return meta_path

    def _load_config_file(self):
        config_file = load_config_file()
        return config_file

    def _get_value_by_key(self, key):
        config_file = self._load_config_file()
        try: 
            value = config_file[key]
        except KeyError: 
            exception_message = "Key was not found in configuration file"
            self.logger.error(exception_message)
            raise ConfigKeyMissing(key, exception_message)
        return value

    def _expand_path_from_string(self, string_path) -> Path:
        path = Path(os.path.expandvars(string_path))
        return path
