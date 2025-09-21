import time
import logging
from typing import Optional
import flask
from models.medical_models import MedicalExtractionInput, MedicalExtractionResult
from interfaces.medical_extractor import MedicalExtractorInterface
from interfaces.response_formatter import ResponseFormatterInterface

class MedicalController:
    """Controller for medical information extraction"""
    
    def __init__(self, 
                 medical_extractor: MedicalExtractorInterface,
                 response_formatter: ResponseFormatterInterface):
        self.medical_extractor = medical_extractor
        self.response_formatter = response_formatter
        self.logger = logging.getLogger(__name__)
    
    def extract_medical_info(self, input_data: MedicalExtractionInput) -> flask.Response:
        """Extract medical information from free text"""
        start_time = time.time()
        
        try:
            self.logger.info(f"Extracting medical information from text: {input_data.text[:100]}...")
            
            # Extract medical information
            extraction_result = self.medical_extractor.extract_medical_info(input_data.text)
            
            # Metadata
            metadata = {
                "processing_time_seconds": round(time.time() - start_time, 2),
                "text_length": len(input_data.text),
                "symptoms_found": len(extraction_result.symptoms)
            }
            
            self.logger.info("Medical information extracted successfully")
            return self.response_formatter.success_response(
                extraction_result.dict(), 
                metadata
            )
            
        except ValueError as e:
            self.logger.error(f"Validation error: {str(e)}")
            return self.response_formatter.error_response(
                str(e), 
                status_code=400,
                error_code="validation_error"
            )
            
        except Exception as e:
            self.logger.error(f"Internal error: {str(e)}")
            return self.response_formatter.error_response(
                "Internal server error",
                status_code=500,
                error_code="internal_error"
            )