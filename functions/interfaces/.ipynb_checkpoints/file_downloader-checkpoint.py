from abc import ABC, abstractmethod

class FileDownloaderInterface(ABC):
    """Interface for file downloaders"""
    
    @abstractmethod
    def download(self, url: str, max_size_mb: int = 50) -> str:
        """Download file and return temporary path"""
        pass
    
    @abstractmethod
    def cleanup(self, file_path: str) -> None:
        """Clean up temporary file"""
        pass