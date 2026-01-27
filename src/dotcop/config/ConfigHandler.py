from dotcop.config.LoadConfigFile import load_config_file
from dotcop.config.LoadDBFile import load_database_file
    
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
        
