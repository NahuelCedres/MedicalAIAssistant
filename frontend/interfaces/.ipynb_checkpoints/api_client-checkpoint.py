from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class APIClientInterface(ABC):
    """Interface para clients que llaman APIs (SRP)"""
    
    @abstractmethod
    def transcribe_audio(self, audio_url: str) -> Dict[str, Any]:
        """Transcribe audio from URL"""
        pass
    
    @abstractmethod
    def extract_medical_info(self, text: str) -> Dict[str, Any]:
        """Extract medical information from text"""
        pass
    
    @abstractmethod
    def generate_diagnosis(self, medical_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate diagnosis from medical data"""
        pass
    
    @abstractmethod
    def set_endpoint(self, service: str, url: str) -> None:
        """Set endpoint URL for specific service"""
        pass
