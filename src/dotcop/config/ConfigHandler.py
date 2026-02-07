from dotcop.config.load_config_file import load_config_file
from dotcop.config.load_db_file import load_database_file
from dotcop.config.load_manifest_dir import load_manifest_dir
from dotcop.config.load_meta_dir import _load_meta_dir

def load_dotcop_config():
    try:
        configuration_file = load_config_file()
    except Exception:
        raise 
    return configuration_file

def load_dotcop_database():
    configuration_file = load_config_file() 
    try:
        database_file = load_database_file(configuration_file)
    except Exception: 
        raise 
    return database_file

def load_dotcop_manifest_directory(): 
    meta_direcotry = _load_dotcop_meta_directory()
    try: 
        manifest_directory = load_manifest_dir(meta_directory)
    except Exception: 
        raise 
    return manifest_directory

def _load_dotcop_meta_directory(): 
    configuration_file = load_config_file() 
    try: 
        meta_directory = _load_meta_dir(configuration_file)
    except Exception: 
        raise 
    return meta_directory
        
