from abc import ABC, abstractmethod
from typing import Dict, Any

class ResultFormatterInterface(ABC):
    """Interface para formatear resultados (SRP)"""
    
    @abstractmethod
    def format_transcription(self, data: Dict[str, Any]) -> None:
        """Format and display transcription results"""
        pass
    
    @abstractmethod
    def format_medical_extraction(self, data: Dict[str, Any]) -> None:
        """Format and display medical extraction results"""
        pass
    
    @abstractmethod
    def format_diagnosis(self, data: Dict[str, Any]) -> None:
        """Format and display diagnosis results"""
        pass
    
    @abstractmethod
    def format_metadata(self, data: Dict[str, Any]) -> None:
        """Format and display metadata"""
        pass