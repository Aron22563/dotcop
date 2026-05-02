from dotcop.config.ConfigHandler import load_config_file
from dotcop.utils.logging_setup import Logger

logger = Logger.get_logger(__name__)

def _load_config_file():
    config_file = load_config_file 
    return config_file

def _get_value_by_key(key):
    config_file = _load_config_file() 
    value = config_file.get(key)
    if value: 
        return value
    logger.error("Value was not found in configuration file: {}", key)
    raise KeyError