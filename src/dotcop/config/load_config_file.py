import os
import yaml
import shutil
from pathlib import Path
from yaml import YAMLError

from dotcop.utils.logging_setup import Logger
from dotcop.utils.root_finder import ROOT
from dotcop.config.exceptions.InvalidEnvironmentVariable import InvalidEnvironmentVariable

logger = Logger.get_logger(__name__)

def load_config_file():
    config_path = _test_config_file()
    try:
        with open(config_path, "r") as file:
            config_file = yaml.safe_load(file)
    except YAMLError as e:
        logger.critical(f"Failed to parse yaml configuration: {e}")
        raise
    return config_file

def _test_config_file():
    # Test if XDG_CONFIG_HOME environment variable exists, if not fail
    expanded_variable = os.environ.get("XDG_CONFIG_HOME")
    if expanded_variable is None:
        raise InvalidEnvironmentVariable("XDG_CONFIG_HOME")

    XDG_CONFIG_HOME = Path(os.environ.get("XDG_CONFIG_HOME"))
    if XDG_CONFIG_HOME is None or not XDG_CONFIG_HOME.is_dir():
        logger.error("XDG_CONFIG_HOME was not found or is incorrect: %s", XDG_CONFIG_HOME)
        raise EnvironmentError()

    # Test if configdir_path exists, if not create it
    configdir_path = XDG_CONFIG_HOME / "dotcop"
    if not configdir_path.is_dir():
        logger.info("No valid configuration directory found at %s", configdir_path)
        try:
            logger.warn("Creating initial configuration directory at %s", configdir_path)
            os.mkdir(configdir_path)
        except (FileExistsError, PermissionError):
            logger.error("Configuration directory could not be created in %s. This could indicate incorrect access rights.", XDG_CONFIG_HOME)
            raise

    # Test if XDG_CONFIG_HOME/dotcop/dotcop.yaml exists, if not copy default configuration from root/conf/.
    config_path = configdir_path / "dotcop.yaml"
    if not config_path.is_file():
        logger.info("No valid configuration file found at %s", config_path)
        src = ROOT / "conf/dotcop.yaml"
        if not src.is_file():
            logger.error("Default configuration file was not found in: %s, please load manually", src)
            raise FileNotFoundError()
        dst = config_path
        try:
            logger.debug("Copying default configuration from %s to %s", src, dst)
            shutil.copyfile(src, dst)
        except PermissionError:
            logger.error("Failed to copy default configuration file from %s to %s", src, dst)
            raise
    return config_path
