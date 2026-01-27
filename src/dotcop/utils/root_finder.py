from pathlib import Path
from dotcop.utils.logging_setup import Logger

def _find_root(start):
  logger = Logger.get_logger(__name__)
  for parent in [start, *start.parents]:
    if (parent / "pyproject.toml").is_file():
      return parent
  logger.error("Could not find pyproject.toml")
  raise FileNotFoundError()

ROOT = _find_root(Path(__file__))