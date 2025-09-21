from abc import ABC, abstractmethod
from typing import Dict, Any
from models.medical_models import MedicalExtractionResult

class MedicalExtractorInterface(ABC):
    """Interface for medical information extractors"""
    
    @abstractmethod
    def extract_medical_info(self, text: str) -> MedicalExtractionResult:
        """Extract medical information from text"""
        pass
    
    @abstractmethod
    def is_ready(self) -> bool:
        """Check if the extractor is ready"""
        pass