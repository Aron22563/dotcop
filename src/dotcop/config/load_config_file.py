import os
import yaml
import shutil
from pathlib import Path
from yaml import YAMLError

from dotcop.utils.logging_setup import Logger
from dotcop.utils.root_finder import ROOT
from dotcop.utils.expand_path import expand_path_from_string

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
    try:
        config_home = expand_path_from_string("$XDG_CONFIG_HOME")
    except PathExpansionFailure:
        logger.error("XDG_CONFIG_HOME environment variable is not set")
        raise
    if not config_home.is_dir():
        logger.error("XDG_CONFIG_HOME environment variable does not point to a directory")
        raise EnvironmentError()

    dotcop_config_path = config_home / "dotcop"
    if not dotcop_config_path.is_dir():
        logger.info("No valid configuration directory found at %s", dotcop_config_path)
        try:
            logger.warn("Creating initial configuration directory at %s", dotcop_config_path)
            os.mkdir(dotcop_config_path)
        except PermissionError:
            logger.error("Dotcop configuration directory could not be created in %s. This could indicate incorrect access rights.", dotcop_config_path)
            raise

    # Test if XDG_CONFIG_HOME/dotcop/dotcop.yaml exists, if not copy default configuration from root/conf/.
    config_path = dotcop_config_path / "dotcop.yaml"
    if not config_path.is_file():
        logger.info("No valid configuration file found at %s", config_path)
        src = ROOT / "conf/dotcop.yaml"
        if not src.is_file():
            logger.error("Default configuration file was not found in: %s, please load manually", src)
            raise FileNotFoundError()
        dst = config_path
        try:
            logger.warn("Copying default configuration from %s to %s", src, dst)
            shutil.copyfile(src, dst)
        except PermissionError:
            logger.error("Failed to copy default configuration file from %s to %s", src, dst)
            raise
    return config_path
