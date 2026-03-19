import os
from pathlib import Path

from dotcop.utils.logging_setup import Logger

logger = Logger.get_logger(__name__)

def _load_meta_dir(configuration_file):
    meta_path = Path(os.path.expandvars(configuration_file['dotcop_meta']))
    meta_path.mkdir(parents=True, exist_ok=True)
    return meta_path
