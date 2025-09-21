import streamlit as st
from typing import Dict, Any
from interfaces.ui_component import UIComponentInterface

class ConfigurationComponent(UIComponentInterface):
    """Configuration component"""
    
    def __init__(self):
        self.config = {
            'transcription_url': "http://localhost:5001/your-project/us-central1/transcribe_audio",
            'extraction_url': "http://localhost:5001/your-project/us-central1/extract_medical_info",
            'diagnosis_url': "http://localhost:5001/your-project/us-central1/generate_diagnosis"
        }
    
    def render(self) -> Dict[str, Any]:
        """Render configuration sidebar"""
        with st.sidebar:
            st.header("⚙️ Configuration")
            
            # API Endpoints
            st.subheader("API Endpoints")
            self.config['transcription_url'] = st.text_input(
                "Transcription API URL", 
                value=self.config['transcription_url'],
                help="Your Firebase transcription function URL"
            )
            
            self.config['extraction_url'] = st.text_input(
                "Medical Extraction API URL", 
                value=self.config['extraction_url'],
                help="Your Firebase medical extraction function URL"
            )
            
            self.config['diagnosis_url'] = st.text_input(
                "Diagnosis API URL", 
                value=self.config['diagnosis_url'],
                help="Your Firebase diagnosis function URL"
            )
            
            st.divider()
            
            # Information about processing
            st.subheader("Processing Information")
            st.info("The system automatically processes the full pipeline: transcription (if audio), medical extraction, and diagnosis generation.")
            st.info("Intermediate results will be shown during processing for transparency.")
        
        return self.config
    
    def validate_input(self, value: Dict[str, Any]) -> bool:
        """Validate configuration"""
        required_urls = ['transcription_url', 'extraction_url', 'diagnosis_url']
        
        for url_key in required_urls:
            url = value.get(url_key, '')
            if not url or not url.startswith(('http://', 'https://')):
                st.error(f"Invalid {url_key}: Must be a valid URL")
                return False
        
        return True