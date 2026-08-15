import os 
from pathlib import Path
from dotcop.utils.logging_setup import Logger
from dotcop.utils.exceptions.PathExpansionFailure import PathExpansionFailure

logger = Logger.get_logger(__name__)

def expand_path_from_string(string_path) -> Path:
        expanded_path = Path(os.path.expandvars(string_path))
        if expanded_path.__str__() == string_path and "$" in string_path: 
            logger.error("Invalid environment variable in path detected: %s", string_path)
            raise PathExpansionFailure(string_path, "Invalid environment variable in path detected")
        return expanded_path