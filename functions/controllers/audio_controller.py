import time
import logging
from typing import Optional
import flask
from models.audio_models import AudioLinkInput, AudioProcessingResult
from interfaces.audio_processor import AudioProcessorInterface
from interfaces.file_downloader import FileDownloaderInterface
from interfaces.response_formatter import ResponseFormatterInterface

class AudioController:
    """Controller for audio processing"""
    
    def __init__(self, 
                 audio_processor: AudioProcessorInterface,
                 file_downloader: FileDownloaderInterface,
                 response_formatter: ResponseFormatterInterface):
        self.audio_processor = audio_processor
        self.file_downloader = file_downloader
        self.response_formatter = response_formatter
        self.logger = logging.getLogger(__name__)
    
    def health_check(self) -> flask.Response:
        """Health check endpoint"""
        health_data = {
            "status": "healthy",
            "processor_ready": self.audio_processor.is_ready(),
            "timestamp": time.time()
        }
        
        return self.response_formatter.success_response(health_data)
    
    def process_audio_from_link(self, input_data: AudioLinkInput) -> flask.Response:
        """Process audio from URL"""
        start_time = time.time()
        temp_file_path: Optional[str] = None  
        
        try:
            self.logger.info(f"Processing audio from: {input_data.audio_url}")
            
            # Download file
            temp_file_path = self.file_downloader.download(
                str(input_data.audio_url), 
                max_size_mb=50
            )
            
            # Process with audio processor
            processing_result = self.audio_processor.process_audio(
                temp_file_path,
                input_data.language,
                input_data.max_duration
            )
            
            # Create structured result
            result = AudioProcessingResult(**processing_result)
            
            # Metadata
            metadata = {
                "processing_time_seconds": round(time.time() - start_time, 2),
                "input_url": str(input_data.audio_url)
            }
            
            self.logger.info("Audio processed successfully")
            return self.response_formatter.success_response(
                result.dict(), 
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
            
        finally:  # Always executes whether there's an error or not
            # Clean up temporary file
            if temp_file_path:
                self.file_downloader.cleanup(temp_file_path)