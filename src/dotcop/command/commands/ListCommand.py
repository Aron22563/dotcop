<<<<<<< Updated upstream
import logging 
logger = logging.getLogger(__name__)

class ListCommand:
    def __init__(self): 
        logger.debug("ListCommand Object created")
=======
from dotcop.utils.logging_setup import Logger

class ListCommand:
    def __init__(self):
        self.logger = Logger.get_logger(__name__)
        self.logger.debug("ListCommand Object created")
>>>>>>> Stashed changes
