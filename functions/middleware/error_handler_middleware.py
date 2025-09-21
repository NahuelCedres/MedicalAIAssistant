import logging
import flask
from werkzeug.exceptions import HTTPException
from interfaces.response_formatter import ResponseFormatterInterface

class ErrorHandlerMiddleware:
    """Error handling middleware (SRP)"""
    
    def __init__(self, app: flask.Flask, response_formatter: ResponseFormatterInterface):
        self.app = app
        self.response_formatter = response_formatter
        self.logger = logging.getLogger(__name__)
        self._register_error_handlers()
    
    def _register_error_handlers(self):
        """Register error handlers"""
        
        @self.app.errorhandler(404)
        def handle_not_found(e):
            return self.response_formatter.error_response(
                "Endpoint not found",
                status_code=404,
                error_code="not_found"
            )
        
        @self.app.errorhandler(405)
        def handle_method_not_allowed(e):
            return self.response_formatter.error_response(
                f"Method {flask.request.method} not allowed for this endpoint",
                status_code=405,
                error_code="method_not_allowed"
            )
        
        @self.app.errorhandler(413)
        def handle_request_too_large(e):
            return self.response_formatter.error_response(
                "Request too large",
                status_code=413,
                error_code="request_too_large"
            )
        
        @self.app.errorhandler(Exception)
        def handle_generic_exception(e):
            self.logger.exception("Unhandled error")
            
            # If it's an HTTP exception, maintain the status code
            if isinstance(e, HTTPException):
                return self.response_formatter.error_response(
                    str(e.description),
                    status_code=e.code,
                    error_code="http_error"
                )
            
            # For internal errors
            return self.response_formatter.error_response(
                "Internal server error",
                status_code=500,
                error_code="internal_error"
            )