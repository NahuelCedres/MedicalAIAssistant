import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class AppConfig:
    """Centralized application configuration (SRP)"""
    
    # File download settings
    download_timeout: int = 30
    max_file_size_mb: int = 50
    max_audio_duration: int = 300  # 5 minutes
    
    # Logging
    log_level: str = "INFO"
    
    # Firebase
    max_instances: int = 10
    
    # OpenAI 
    openai_api_key: str = ""
    audio_processor_type: str = "openai"
    medical_model: str = "gpt-4"
    max_symptoms: int = 5
    
    # Perplexity
    perplexity_api_key: str = ""
    perplexity_model: str = "sonar"
    
    @classmethod
    def from_environment(cls) -> 'AppConfig':
        """Create configuration from environment variables"""
        return cls(
            download_timeout=int(os.getenv('DOWNLOAD_TIMEOUT', cls.download_timeout)),
            max_file_size_mb=int(os.getenv('MAX_FILE_SIZE_MB', cls.max_file_size_mb)),
            max_audio_duration=int(os.getenv('MAX_AUDIO_DURATION', cls.max_audio_duration)),
            log_level=os.getenv('LOG_LEVEL', cls.log_level),
            max_instances=int(os.getenv('MAX_INSTANCES', cls.max_instances)),
            openai_api_key=os.getenv('OPENAI_API_KEY', cls.openai_api_key),
            audio_processor_type=os.getenv('AUDIO_PROCESSOR_TYPE', cls.audio_processor_type),
            medical_model=os.getenv('MEDICAL_MODEL', cls.medical_model),
            max_symptoms=int(os.getenv('MAX_SYMPTOMS', cls.max_symptoms)),
            perplexity_api_key=os.getenv('PERPLEXITY_API_KEY', cls.perplexity_api_key),
            perplexity_model=os.getenv('PERPLEXITY_MODEL', cls.perplexity_model),
        )