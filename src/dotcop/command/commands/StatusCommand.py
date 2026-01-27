import os
import yaml
from pathlib import Path
from yaml import YAMLError

from dotcop.utils.logging_setup import Logger
from dotcop.config.ConfigHandler import load_dotcop_config, load_dotcop_database

class StatusCommand:
    def __init__(self):
        self.logger = Logger.get_logger(__name__) 
        self.config_file = load_dotcop_config()
        
    def run(self, args):
        database_file = load_dotcop_database()
        self.logger.info("Database file was loaded by StatusCommand")
