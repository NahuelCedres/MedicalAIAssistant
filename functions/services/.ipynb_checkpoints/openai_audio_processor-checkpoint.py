import requests
import os
import logging
from typing import Dict, Any, Optional
from interfaces.audio_processor import AudioProcessorInterface

class OpenAIAudioProcessor(AudioProcessorInterface):
    def __init__(self, api_key: str, model: str = "whisper-1"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.openai.com/v1/audio/transcriptions"
        self.logger = logging.getLogger(__name__)
    
    def process_audio(self, file_path: str, language: Optional[str] = None, 
                     max_duration: int = 300) -> Dict[str, Any]:
        
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")
        
        try:
            self.logger.info(f"Sending audio to OpenAI API: {file_path}")
            
            # Verify file exists
            if not os.path.exists(file_path):
                raise ValueError(f"File not found: {file_path}")
            
            # Prepare the request
            with open(file_path, 'rb') as audio_file:
                # Get base filename for Content-Type
                content_type = self._get_content_type(file_path)
                filename = os.path.basename(file_path)
                
                files = {
                    'file': (filename, audio_file, content_type),
                    'model': (None, self.model),
                    'response_format': (None, 'json'),
                }
                
                # Add language if specified
                if language:
                    # Map languages to ISO codes
                    lang_map = {
                        "spanish": "es",
                        "english": "en", 
                        "french": "fr",
                        "german": "de",
                        "italian": "it"
                    }
                    lang_code = lang_map.get(language.lower(), language.lower()[:2])
                    files['language'] = (None, lang_code)
                
                headers = {
                    'Authorization': f'Bearer {self.api_key}'
                }
                
                self.logger.debug(f"Request headers: {headers}")
                self.logger.debug(f"Request files keys: {list(files.keys())}")
                
                # Make the request
                response = requests.post(
                    self.base_url, 
                    files=files, 
                    headers=headers,
                    timeout=60
                )
                
                self.logger.info(f"OpenAI API response status: {response.status_code}")
                
                # Log error for debugging
                if response.status_code != 200:
                    self.logger.error(f"OpenAI API Error: {response.status_code}")
                    self.logger.error(f"Response content: {response.text}")
                    response.raise_for_status()
                
                result = response.json()
                self.logger.info("Transcription completed successfully")
                
                return {
                    "transcription": result.get("text", ""),
                    "duration_seconds": result.get("duration", 0),
                    "language_detected": language or "auto",
                    "model_used": "openai-whisper-1"
                }
    
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error in request to OpenAI: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                self.logger.error(f"Response content: {e.response.text}")
            raise ValueError(f"Error communicating with OpenAI API: {str(e)}")
        
        except Exception as e:
            self.logger.error(f"Error processing audio: {str(e)}")
            raise ValueError(f"Error in processing: {str(e)}")

    def _get_content_type(self, file_path: str) -> str:
        """Get correct Content-Type based on file extension"""
        ext = os.path.splitext(file_path)[1].lower()
        content_types = {
            '.mp3': 'audio/mpeg',
            '.wav': 'audio/wav',
            '.mp4': 'audio/mp4',
            '.m4a': 'audio/m4a',
            '.ogg': 'audio/ogg',
            '.flac': 'audio/flac',
            '.webm': 'audio/webm',
        }
        return content_types.get(ext, 'audio/mpeg')   
    
    def is_ready(self) -> bool:
        ready = bool(self.api_key)
        self.logger.debug(f"OpenAI processor ready: {ready}")
        return ready