import flask
from functools import wraps
from typing import Type, Callable
from pydantic import BaseModel, ValidationError
from interfaces.response_formatter import ResponseFormatterInterface

class ValidationMiddleware:
    """Data validation middleware (OCP)"""
    
    def __init__(self, response_formatter: ResponseFormatterInterface):
        self.response_formatter = response_formatter
    
    def validate_json(self, model_class: Type[BaseModel]) -> Callable:
        """Decorator to validate JSON with Pydantic"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not flask.request.is_json:
                    return self.response_formatter.error_response(
                        "Content-Type must be application/json",
                        status_code=415,
                        error_code="invalid_content_type"
                    )
                
                try:
                    json_data = flask.request.get_json()
                    if not json_data:
                        return self.response_formatter.error_response(
                            "JSON body required",
                            status_code=400,
                            error_code="empty_body"
                        )
                    
                    validated_data = model_class(**json_data)
                    flask.g.validated_data = validated_data
                    return func(*args, **kwargs)
                    
                except ValidationError as e:
                    return self.response_formatter.error_response(
                        f"Invalid data: {str(e)}",
                        status_code=422,
                        error_code="validation_error"
                    )
                except Exception as e:
                    return self.response_formatter.error_response(
                        f"Error processing JSON: {str(e)}",
                        status_code=400,
                        error_code="json_error"
                    )
            
            return wrapper
        return decorator