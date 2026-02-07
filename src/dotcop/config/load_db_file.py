import os
import yaml
import shutil
from pathlib import Path
from yaml import YAMLError

from dotcop.utils.logging_setup import Logger
from dotcop.utils.root_finder import ROOT

logger = Logger.get_logger(__name__)

def _test_database_file(configuration_file):
    database_path = Path(os.path.expandvars(configuration_file['dotcop_database']))

    if database_path.is_file(): 
        return database_path
    
    database_path.parent.mkdir(parents=True, exist_ok=True)
    src = ROOT / "conf/package_db.yaml"
    if not src.is_file(): 
        logger.critical(f"Default package database file was not found in: {src}, please load manually")
        raise FileNotFoundError()
    dst = database_path
    try: 
        logger.debug(f"Copying default package database file from {src} to {dst}")
        shutil.copyfile(src, dst)
    except PermissionError: 
        logger.critical(f"Failed to copy default package database file from {src} to {dst}")
        raise 
    return database_path

def load_database_file(configuration_file): 
    database_path = _test_database_file(configuration_file)
    try:
        with open(database_path, "r") as file:
            database_file = yaml.safe_load(file)
    except YAMLError as e:
        logger.critical(f"Failed to parse package database file from: {database_path}")
        raise
    return database_file