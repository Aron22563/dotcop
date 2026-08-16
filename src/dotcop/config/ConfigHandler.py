from dotcop.config.load_config_file import load_config_file
from dotcop.config.load_db_file import load_database_file
from dotcop.config.load_manifest_dir import load_manifest_dir
from dotcop.config.load_meta_dir import load_meta_dir

def load_dotcop_config():
    try:
        configuration_file = load_config_file()
    except Exception:
        raise
    return configuration_file

def load_dotcop_database(database_path):
    try:
        database_file = load_database_file(database_path)
    except Exception:
        raise
    return database_file

def load_dotcop_manifest_directory(meta_path):
    meta_directory = _load_dotcop_meta_directory(meta_path)
    try:
        manifest_directory = load_manifest_dir(meta_directory)
    except FileExistsError:
        raise
    return manifest_directory

def _load_dotcop_meta_directory(meta_path):
    try:
        meta_directory = load_meta_dir(meta_path)
    except FileExistsError:
        raise
    return meta_directory
