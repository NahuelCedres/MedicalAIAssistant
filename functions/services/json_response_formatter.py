import flask
from datetime import datetime, timezone
from typing import Dict, Any
from interfaces.response_formatter import ResponseFormatterInterface

class JSONResponseFormatter(ResponseFormatterInterface):
    """JSON response formatter implementation"""
    
    def success_response(self, data: Dict[str, Any], 
                        metadata: Dict[str, Any] = None) -> flask.Response:
        """Format successful response"""
        response_data = {
            "success": True,
            "result": data,
            "metadata": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                **(metadata or {})
            }
        }
        
        return flask.jsonify(response_data)
    
    def error_response(self, message: str, status_code: int = 400, 
                      error_code: str = None) -> flask.Response:
        """Format error response"""
        response_data = {
            "success": False,
            "error": {
                "message": message,
                "code": error_code or "generic_error",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        }
        
        response = flask.jsonify(response_data)
        response.status_code = status_code
        return response