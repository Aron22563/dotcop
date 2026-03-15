<<<<<<< Updated upstream
import logging 
logger = logging.getLogger(__name__)

class CreateCommand:
    def __init__(self): 
        logger.debug("CreateCommand Object created")
=======
from dotcop.utils.logging_setup import Logger

class CreateCommand:
    def __init__(self):
        self.logger = Logger.get_logger(__name__)
        self.logger.debug("CreateCommand Object created")
>>>>>>> Stashed changes
