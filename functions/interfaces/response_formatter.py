from abc import ABC, abstractmethod
from typing import Dict, Any
import flask

class ResponseFormatterInterface(ABC):
    """Interface for response formatting"""
    
    @abstractmethod
    def success_response(self, data: Dict[str, Any], 
                        metadata: Dict[str, Any] = None) -> flask.Response:
        """Format successful response"""
        pass
    
    @abstractmethod
    def error_response(self, message: str, status_code: int = 400, 
                      error_code: str = None) -> flask.Response:
        """Format error response"""
        pass