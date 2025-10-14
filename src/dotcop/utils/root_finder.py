from pathlib import Path 
from dotcop.logging_setup import Logger 

# Finds project root by finding pyproject.toml in the project root. This breaks if pyproject.toml is moved.

class RootFinder: 
    def __init__(self):
        self.logger = Logger.get_logger(__name__)

    def find_root(self, start: Path | None = None) -> Path:
        current = start or Path.cwd()
        for parent in [current, *current.parents]:
            if(parent / "pyproject.toml").exists():
                return parent
        self.logger.critical("Finding root folder failed, pyproject.toml not found")
        raise FileNotFoundError()
