import datetime
import hashlib
import yaml
import os
from pathlib import Path
from dotcop.config.ConfigHandler import load_dotcop_manifest_directory
from dotcop.utils.logging_setup import Logger

logger = Logger.get_logger(__name__)

class Linker:
    def __init__(self, package_folder):
        self.manifest_file_path = None
        self.manifest_data = {}
        self._init_manifest_file(package_folder)

    def link(self, src_path, dst_path):
        self._write_to_manifest(src_path, dst_path)
        self._write_symlink(src_path, dst_path)

    def _init_manifest_file(self, package_folder):
        self.time_stamp = datetime.datetime.now().replace(microsecond=0).isoformat()
        manifest_directory = load_dotcop_manifest_directory()
        package_manifest_path = manifest_directory / package_folder
        package_manifest_path.mkdir(parents=True, exist_ok=True)

        manifest_file_name = f"manifest-{self.time_stamp}.yaml"
        self.manifest_file_path = package_manifest_path / manifest_file_name
        self.manifest_file_path.touch(exist_ok=True)
        
        self.manifest_data = {"created_at": self.time_stamp, "entries": {}}


    def _write_to_manifest(self, src_path, dst_path):
        timestamp = datetime.datetime.now().replace(microsecond=0).isoformat()
        hash_input = f"{src_path}|{dst_path}|{timestamp}"
        entry_key = hashlib.sha256(hash_input.encode()).hexdigest()[:8]

        self.manifest_data["entries"][entry_key] = {
            "src": str(src_path),
            "dst": str(dst_path),
            "timestamp": timestamp
        }
        try: 
            with open(self.manifest_file_path, "w") as f:
                yaml.safe_dump(self.manifest_data, f, sort_keys=False)
        except Exception as e:
            logger.error(f"Failed to write manifest {self.manifest_file_path}")
            raise    
        
    def _write_symlink(self, src_path, dst_path):
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            if dst_path.exists() or dst_path.is_symlink():
                dst_path.unlink()

            os.symlink(src_path, dst_path)
            logger.info(f"Symlink created: {src_path} -> {dst_path}")

        except Exception as e:
            logger.error(f"Failed to create symlink {src_path} -> {dst_path}: {e}")
            raise
        
