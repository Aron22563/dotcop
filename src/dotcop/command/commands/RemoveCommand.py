<<<<<<< Updated upstream
import logging 
logger = logging.getLogger(__name__)

class RemoveCommand:
    def __init__(self): 
        logger.debug("RemoveCommand Object created")
=======
from dotcop.utils.logging_setup import Logger

class RemoveCommand:
    def __init__(self):
        self.logger = Logger.get_logger(__name__)
        self.logger.debug("RemoveCommand Object created")
>>>>>>> Stashed changes
