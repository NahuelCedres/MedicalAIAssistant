import streamlit as st
from typing import Optional
from interfaces.ui_component import UIComponentInterface

class TextInputComponent(UIComponentInterface):
    """Component para input de texto (SRP)"""
    
    def __init__(self, title: str = "Direct Text Input", height: int = 200):
        self.title = title
        self.height = height
        self.text_value = None
    
    def render(self) -> Optional[str]:
        """Render text input component"""
        st.subheader(self.title)
        
        text_input = st.text_area(
            "Enter medical consultation text:",
            height=self.height,
            placeholder="Patient presents with chest pain, shortness of breath...",
            key="text_input_area"
        )
        
        self.text_value = text_input
        return text_input if text_input.strip() else None
    
    def validate_input(self, value: str) -> bool:
        """Validate text input"""
        if not value or not value.strip():
            return False
        
        # Minimum length check
        if len(value.strip()) < 10:
            st.error("Please provide at least 10 characters of medical text")
            return False
        
        # Basic medical context check (optional)
        medical_keywords = [
            'patient', 'symptoms', 'pain', 'diagnosis', 'treatment', 
            'medical', 'doctor', 'nurse', 'hospital', 'clinic',
            'presents', 'complains', 'reports', 'examination'
        ]
        
        text_lower = value.lower()
        if not any(keyword in text_lower for keyword in medical_keywords):
            st.warning("Text doesn't appear to contain medical content. Continue anyway?")
        
        return True