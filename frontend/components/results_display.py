import streamlit as st
from typing import Dict, Any, List
from interfaces.ui_component import UIComponentInterface
from interfaces.result_formatter import ResultFormatterInterface

class ResultsDisplayComponent(UIComponentInterface):
    """Results Display Component"""
    
    def __init__(self, formatter: ResultFormatterInterface):
        self.formatter = formatter 
        self.results_data = None
    
    def render(self, results: Dict[str, Any]) -> None:
        """Render results with tabs"""
        self.results_data = results
        
        # Create tabs based on available results
        tab_names = []
        if 'transcription' in results:
            tab_names.append("🎵 Transcription")
        if 'extraction' in results:
            tab_names.append("📋 Medical Data")
        if 'diagnosis' in results:
            tab_names.append("🩺 Diagnosis")
        
        if not tab_names:
            st.warning("No results to display")
            return
        
        tabs = st.tabs(tab_names)
        tab_index = 0
        
        # Transcription tab
        if 'transcription' in results:
            with tabs[tab_index]:
                self.formatter.format_transcription(results['transcription'])
            tab_index += 1
        
        # Medical extraction tab
        if 'extraction' in results:
            with tabs[tab_index]:
                self.formatter.format_medical_extraction(results['extraction'])
            tab_index += 1
        
        # Diagnosis tab
        if 'diagnosis' in results:
            with tabs[tab_index]:
                self.formatter.format_diagnosis(results['diagnosis'])
            tab_index += 1
    
    def validate_input(self, value: Dict[str, Any]) -> bool:
        """Validate results data structure"""
        if not isinstance(value, dict):
            return False
        
        # Check if at least one result type exists
        valid_keys = ['transcription', 'extraction', 'diagnosis']
        return any(key in value for key in valid_keys)
    
    def render_error(self, error_message: str, partial_results: Dict[str, Any] = None):
        """Render error state (LSP)"""
        st.error(f"Processing failed: {error_message}")
        
        if partial_results:
            st.warning("Partial results available:")
            self.render(partial_results)
    
    def render_processing_state(self, message: str):
        """Render processing state (LSP)"""
        st.info(message)
        st.spinner("Processing...")
