from abc import ABC, abstractmethod

class ConfigFileInterface(ABC):
    """
    Interface for retrieving values from the configuration file
    """
    @abstractmethod
    def get_name_field(self) -> str:
        """ Retrieve the 'name' field from the configuration file"""

    @abstractmethod
    def get_log_path(self) -> str:
        """ Retrieve the 'log_path' field from the configuration file"""

    @abstractmethod
    def get_package_path(self) -> str:
        """ Retrieve the 'package_path' field from the configuration file"""

    @abstractmethod
    def get_database_path(self) -> str:
        """ Retrieve the 'database_path' field from the configuration file"""

    @abstractmethod
    def get_meta_path(self) -> str:
        """ Retrieve the 'meta_path' field from the configuration file"""
