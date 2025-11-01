import os
import yaml
import shutil
from pathlib import Path
from yaml import YAMLError
from dotcop.utils.logging_setup import Logger
from dotcop.utils.root_finder import RootFinder


class Config:
    def __init__(self):
        self.logger = Logger.get_logger(__name__)

    def test_configfile(self):
        self.logger.debug("Writing configuration file...")
        # Test if XDG_CONFIG_HOME environment variable exists, if not fail
        XDG_CONFIG_HOME = os.environ.get("XDG_CONFIG_HOME")
        if XDG_CONFIG_HOME is None or not Path(XDG_CONFIG_HOME).is_dir():
            self.logger.critical(f"XDG_CONFIG_HOME was not found or is incorrect: {XDG_CONFIG_HOME}")
            raise EnvironmentError()

        # Test if configdir_path exists, if not create it
        configdir_path = Path(XDG_CONFIG_HOME) / "dotcop"
        if not configdir_path.is_dir():
            self.logger.info(f"No valid configuration directory found at {configdir_path}")
            try:
                self.logger.debug(f"Creating configuration directory at {configdir_path}")
                os.mkdir(configdir_path)
            except (FileExistsError, PermissionError):
                self.logger.critical(
                    f'Configuration directory "dotcop" could not be created in {XDG_CONFIG_HOME}. This could indicate incorrect access rights.'
                )
                raise

        # Test if XDG_CONFIG_HOME/dotcop/dotcop.yml exists, if not copy default configuration from project root.
        config_path = configdir_path / "dotcop.yml"
        if not config_path.is_file():
            self.logger.info(f"No valid configuration file found at {config_path}")
            try:
                root_path = RootFinder().find_root()
            except FileNotFoundError:
                raise
            src = root_path / "dotcop.yml"
            if not src.is_file():
                self.logger.critical(f"Default configuration file was not found in project root: {src}")
                raise FileNotFoundError()
            dst = config_path
            try:
                self.logger.debug(f"Copying default configuration from {dst} to {src}")
                shutil.copyfile(src, dst)
            except PermissionError:
                self.logger.critical(f"Failed to copy default configuration file from {dst} to {src}")
                raise
        self.config_path = config_path

    def load_configfile(self):
        try:
            self.test_configfile()
        except Exception:
            raise
        try:
            with open(self.config_path, "r") as file:
                config_file = yaml.safe_load(file)
        except YAMLError as e:
            self.logger.critical(f"Failed to parse yaml configuration: {e}")
            raise
        return config_file
