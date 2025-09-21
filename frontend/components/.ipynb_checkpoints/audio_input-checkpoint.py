import streamlit as st
from typing import Optional, Dict, Any
from interfaces.ui_component import UIComponentInterface

class AudioInputComponent(UIComponentInterface):
    """Audio Input Component"""
    
    def __init__(self, title: str = "Upload Audio File"):
        self.title = title
        self.audio_url = None
    
    def render(self) -> Optional[str]:
        """Render audio input component"""
        st.subheader(self.title)
        
        # Audio URL input
        audio_url = st.text_input(
            "Audio File URL",
            placeholder="https://example.com/audio.wav",
            help="Provide a direct URL to your audio file",
            key="audio_url_input"
        )
        
        self.audio_url = audio_url
        return audio_url if audio_url else None
    
    def validate_input(self, value: str) -> bool:
        """Validate audio URL"""
        if not value:
            return False
        
        # Basic URL validation
        if not value.startswith(('http://', 'https://')):
            st.error("Please provide a valid URL starting with http:// or https://")
            return False
        
        return True