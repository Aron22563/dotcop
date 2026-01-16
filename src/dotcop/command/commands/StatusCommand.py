from dotcop.utils.logging_setup import Logger

import os
from pathlib import Path

class StatusCommand:
    def __init__(self): 
        self.logger = Logger.get_logger(__name__)
        self.logger.debug("StatusCommand Object created")
        
    def run(self, args, config): 
        package_path = os.path.expandvars(config['package_path'])
        if not Path(package_path).is_dir():
            self.logger.error(f"Package path is not a directory: {package_path}")