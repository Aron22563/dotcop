import os
import yaml
import shutil
from pathlib import Path
from yaml import YAMLError

from dotcop.utils.logging_setup import Logger
from dotcop.utils.root_finder import ROOT

logger = Logger.get_logger(__name__)

def _test_config_file():
    logger.debug("Writing configuration file...")
    # Test if XDG_CONFIG_HOME environment variable exists, if not fail
    XDG_CONFIG_HOME = os.environ.get("XDG_CONFIG_HOME")
    if XDG_CONFIG_HOME is None or not Path(XDG_CONFIG_HOME).is_dir():
        logger.critical(f"XDG_CONFIG_HOME was not found or is incorrect: {XDG_CONFIG_HOME}")
        raise EnvironmentError()

    # Test if configdir_path exists, if not create it
    configdir_path = Path(XDG_CONFIG_HOME) / "dotcop"
    if not configdir_path.is_dir():
        logger.info(f"No valid configuration directory found at {configdir_path}")
        try:
            logger.debug(f"Creating configuration directory at {configdir_path}")
            os.mkdir(configdir_path)
        except (FileExistsError, PermissionError):
            logger.critical(
                f'Configuration directory "dotcop" could not be created in {XDG_CONFIG_HOME}. This could indicate incorrect access rights.'
            )
            raise

    # Test if XDG_CONFIG_HOME/dotcop/dotcop.yaml exists, if not copy default configuration from root/conf/.
    config_path = configdir_path / "dotcop.yaml"
    if not config_path.is_file():
        logger.info(f"No valid configuration file found at {config_path}")
        src = ROOT / "conf/dotcop.yaml"
        if not src.is_file():
            logger.critical(f"Default configuration file was not found in: {src}, please load manually")
            raise FileNotFoundError()
        dst = config_path
        try:
            logger.debug(f"Copying default configuration from {src} to {dst}")
            shutil.copyfile(src, dst)
        except PermissionError:
            logger.critical(f"Failed to copy default configuration file from {src} to {dst}")
            raise
    return config_path

def load_config_file():
    config_path = _test_config_file()
    try:
        with open(config_path, "r") as file:
            config_file = yaml.safe_load(file)
    except YAMLError as e:
        logger.critical(f"Failed to parse yaml configuration: {e}")
        raise
    return config_file
