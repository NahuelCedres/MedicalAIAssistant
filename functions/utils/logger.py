import logging
import sys
from typing import Optional

class Logger:
    """Logging"""
    
    @staticmethod
    def setup_logging(level: str = "INFO", 
                     format_string: Optional[str] = None) -> None:
        """Loggin Configuritation"""
        
        if format_string is None:
            format_string = (
                '%(asctime)s - %(name)s - %(levelname)s - '
                '%(funcName)s:%(lineno)d - %(message)s'
            )
        
        logging.basicConfig(
            level=getattr(logging, level.upper()),
            format=format_string,
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        logging.getLogger('transformers').setLevel(logging.WARNING)
        logging.getLogger('torch').setLevel(logging.WARNING)
        logging.getLogger('librosa').setLevel(logging.WARNING)