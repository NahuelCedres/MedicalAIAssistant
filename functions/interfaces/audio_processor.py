from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class AudioProcessorInterface(ABC):
    """Interface for audio processors"""
    
    @abstractmethod
    def process_audio(self, file_path: str, language: Optional[str] = None, 
                     max_duration: int = 300) -> Dict[str, Any]:
        """Process audio file and return transcription"""
        pass
    
    @abstractmethod
    def is_ready(self) -> bool:
        """Check if the processor is ready"""
        pass