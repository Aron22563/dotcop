import os
from pathlib import Path

from dotcop.utils.logging_setup import Logger

logger = Logger.get_logger(__name__)

def load_manifest_dir(meta_path):
    manifest_path = meta_path / "manifests"
    try:
        manifest_path.mkdir(parents=True, exist_ok=True)
    except FileExistsError: 
        logger.error("Found file instead of directory at manifest path: %s", manifest_path)
        raise
    return manifest_path
