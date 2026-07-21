from dotcop.config.ConfigHandler import load_database_file
from dotcop.utils.logging_setup import Logger

logger = Logger.get_logger(__name__)

def _load_database_file():
    database_file = load_database_file
    return database_file

def _get_value_by_key(key):
    database_file = _load_database_file()
    value = database_file.get(key)
    if value:
        return value
    logger.error("Value was not found in database file: {}", key)
    raise KeyError
