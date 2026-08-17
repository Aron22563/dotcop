import yaml
import shutil
from pathlib import Path
from yaml import YAMLError

from dotcop.utils.logging_setup import Logger
from dotcop.utils.root_finder import ROOT

logger = Logger.get_logger(__name__)

def load_database_file(database_path):
    database_path = _test_database_file(database_path)
    try:
        with open(database_path, "r") as file:
            database_file = yaml.safe_load(file)
    except YAMLError:
        logger.critical(f"Failed to parse package database file from: {database_path}")
        raise
    return database_file

def _test_database_file(database_path) -> Path:
    if database_path.is_file():
        return database_path

    database_path.parent.mkdir(parents=True, exist_ok=True)
    src = ROOT / "conf/package_db.yaml"
    if not src.is_file():
        logger.critical("Default package database file was not found in: %s, please load manually", src)
        raise FileNotFoundError()
    dst = database_path
    try:
        logger.warn("Copying default package database file from %s to %s", src, dst)
        shutil.copyfile(src, dst)
    except PermissionError:
        logger.critical("Failed to copy default package database file from %s to %s", src, dst)
        raise
    return database_path


