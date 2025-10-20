import argparse 
from dotcop.utils.logging_setup import Logger

class Parser: 
    def __init__(self): 
        self.logger = Logger.get_logger(__name__)

    def test_arguments(self): 
        print("test_arguments was called")
    
    def parse_arguments(self): 
        try: 
            test_arguments()
            call_task()            
        except Exception as e: 
            raise
