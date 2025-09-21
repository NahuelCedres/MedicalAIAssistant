import os
import tempfile
import requests
import logging
from interfaces.file_downloader import FileDownloaderInterface

class HTTPFileDownloader(FileDownloaderInterface):
    """HTTP file downloader implementation"""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; AudioProcessor/1.0)'
        }
    
    def download(self, url: str, max_size_mb: int = 50) -> str:
        """Download file from URL"""
        try:
            self.logger.info(f"Downloading: {url}")
            
            response = requests.get(url, headers=self._headers, 
                                  stream=True, timeout=self.timeout)
            response.raise_for_status()
            
            # Check file size
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > max_size_mb * 1024 * 1024:
                raise ValueError(f"File too large. Maximum: {max_size_mb}MB")
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            
            downloaded_size = 0
            max_size_bytes = max_size_mb * 1024 * 1024
            
            for chunk in response.iter_content(chunk_size=8192):
                downloaded_size += len(chunk)
                if downloaded_size > max_size_bytes:
                    temp_file.close()
                    os.unlink(temp_file.name)
                    raise ValueError(f"File too large during download")
                
                temp_file.write(chunk)
            
            temp_file.close()
            self.logger.info(f"File downloaded: {temp_file.name}")
            return temp_file.name
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error downloading: {str(e)}")
            raise ValueError(f"Download error: {str(e)}")
    
    def cleanup(self, file_path: str) -> None:
        """Clean up temporary file"""
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
                self.logger.info(f"File cleaned up: {file_path}")
        except Exception as e:
            self.logger.warning(f"Error cleaning up file {file_path}: {str(e)}")