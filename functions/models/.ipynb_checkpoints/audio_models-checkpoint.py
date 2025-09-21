from pydantic import BaseModel, HttpUrl, Field, validator
from typing import Optional
from datetime import datetime

class AudioLinkInput(BaseModel):
    """Model for audio processing input"""
    audio_url: HttpUrl = Field(..., description="Audio file URL")
    language: Optional[str] = Field(None, description="Audio language")
    max_duration: Optional[int] = Field(300, ge=1, le=1800, 
                                       description="Maximum duration in seconds")
    
    @validator('language')
    def validate_language(cls, v):
        if v is not None:
            allowed_languages = ['spanish', 'english', 'french', 'german', 'italian']
            if v.lower() not in allowed_languages:
                raise ValueError(f'Language must be one of: {allowed_languages}')
        return v.lower() if v else v
    
    class Config:
        json_schema_extra = {
            "example": {
                "audio_url": "https://example.com/audio.mp3",
                "language": "spanish",
                "max_duration": 300
            }
        }

class AudioProcessingResult(BaseModel):
    """Model for processing result"""
    transcription: str
    duration_seconds: float
    language_detected: str
    model_used: str
    confidence_score: Optional[float] = None

class AudioProcessingResponse(BaseModel):
    """Model for complete response"""
    success: bool
    result: Optional[AudioProcessingResult] = None
    error: Optional[str] = None
    metadata: Optional[dict] = None
    
    @validator('result')
    def validate_result(cls, v, values):
        if values.get('success') and not v:
            raise ValueError('Result is required when success is True')
        return v