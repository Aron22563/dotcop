
from dotcop.utils.logging_setup import Logger

logger = Logger.get_logger(__name__)

def load_meta_dir(meta_path):
    try:
        meta_path.mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        logger.error("Found file instead of directory at meta path: %s", meta_path)
        raise
    return meta_path
