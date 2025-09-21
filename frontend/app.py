# Streamlit
import streamlit as st
from typing import Dict, Any, Optional

# interfaces
from interfaces.api_client import APIClientInterface
from interfaces.result_formatter import ResultFormatterInterface

# implementations
from services.firebase_client import FirebaseAPIClient
from services.data_processor import DataProcessor
from utils.formatters import MedicalResultFormatter
from utils.styles import AppStyles
from components.audio_input import AudioInputComponent
from components.text_input import TextInputComponent
from components.results_display import ResultsDisplayComponent
from components.configuration import ConfigurationComponent

class MedicalAIApp:
    """
    Main application class that orchestrates all components (SRP)
    Uses dependency injection for all services (DIP)
    """
    
    def __init__(self):
        """Initialize app with dependency injection"""
        # Initialize services 
        self.api_client: APIClientInterface = FirebaseAPIClient()
        self.formatter: ResultFormatterInterface = MedicalResultFormatter()
        self.data_processor = DataProcessor(self.api_client)
        
        # Initialize UI components
        self.audio_component = AudioInputComponent()
        self.text_component = TextInputComponent()
        self.results_component = ResultsDisplayComponent(self.formatter)
        self.config_component = ConfigurationComponent()
        
        # Initialize session state
        self._initialize_session_state()
    
    def _initialize_session_state(self) -> None:
        """Initialize Streamlit session state"""
        if 'processing_results' not in st.session_state:
            st.session_state.processing_results = {}
        if 'app_config' not in st.session_state:
            st.session_state.app_config = {}
    
    def configure_page(self) -> None:
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="Medical AI Assistant",
            page_icon="🏥",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Load custom styles
        AppStyles.load_custom_css()
    
    def render_header(self) -> None:
        """Render application header"""
        AppStyles.render_header("🏥 Medical AI Assistant")
    
    def handle_configuration(self) -> Dict[str, Any]:
        """Handle configuration sidebar (SRP)"""
        config = self.config_component.render()
        
        if self.config_component.validate_input(config):
            # Update API client endpoints
            self.api_client.set_endpoint('transcription', config['transcription_url'])
            self.api_client.set_endpoint('extraction', config['extraction_url'])
            self.api_client.set_endpoint('diagnosis', config['diagnosis_url'])
            
            st.session_state.app_config = config
        
        return config
    
    def render_input_section(self) -> tuple[Optional[str], Optional[str]]:
        """Render input section and return user inputs"""
        AppStyles.render_section_header("📤 Input Methods")
        
        # Input method selection
        input_method = st.radio(
            "Choose input method:",
            ["🎵 Audio Upload", "✏️ Text Input"],
            horizontal=True
        )
        
        audio_url = None
        text_input = None
        
        if input_method == "🎵 Audio Upload":
            audio_url = self.audio_component.render()
            if audio_url and not self.audio_component.validate_input(audio_url):
                audio_url = None
        else:
            text_input = self.text_component.render()
            if text_input and not self.text_component.validate_input(text_input):
                text_input = None
        
        # Process button
        st.markdown("---")
        if st.button("🔬 Process Medical Data", type="primary", use_container_width=True):
            if not audio_url and not text_input:
                st.error("Please provide either an audio URL or text input!")
            else:
                self.process_medical_data(audio_url, text_input)
        
        return audio_url, text_input
    
    def process_medical_data(self, audio_url: Optional[str], text_input: Optional[str]) -> None:
        """Process medical data through the AI pipeline"""
        if not audio_url and not text_input:
            st.error("Please provide either an audio URL or text input!")
            return
        
        # Create progress callback
        def show_progress(message: str):
            AppStyles.render_processing_step(message)
        
        # Process data using the data processor service
        with st.spinner("Processing your medical data..."):
            result = self.data_processor.process_full_pipeline(
                audio_url=audio_url,
                text_input=text_input,
                show_progress_callback=show_progress
            )
            
            if result['success']:
                st.session_state.processing_results = result['results']
                AppStyles.render_success_message("Processing completed successfully!")
                
                # Always show intermediate results for better UX
                self._show_intermediate_results(result['results'])
            else:
                error_message = result.get('error', 'Unknown error occurred')
                AppStyles.render_error_message(f"Processing failed: {error_message}")
                
                # Show partial results if available
                if 'partial_results' in result:
                    st.warning("Partial results available:")
                    st.session_state.processing_results = result['partial_results']
    
    def _show_intermediate_results(self, results: Dict[str, Any]) -> None:
        """Show intermediate processing results"""
        if 'transcription' in results:
            with st.expander("📝 Transcription Result", expanded=False):
                transcription = results['transcription'].get('result', {}).get('transcription', '')
                st.write(transcription[:200] + "..." if len(transcription) > 200 else transcription)
        
        if 'extraction' in results:
            with st.expander("📋 Medical Extraction Result", expanded=False):
                extraction_result = results['extraction'].get('result', {})
                if 'symptoms' in extraction_result:
                    st.write("**Symptoms found:**", extraction_result['symptoms'])
    
    def render_results_section(self) -> None:
        """Render results section"""
        if st.session_state.processing_results:
            AppStyles.render_section_header("📊 Results")
            
            try:
                if self.results_component.validate_input(st.session_state.processing_results):
                    self.results_component.render(st.session_state.processing_results)
                else:
                    st.error("Invalid results data structure")
            except Exception as e:
                self.results_component.render_error(
                    f"Error displaying results: {str(e)}",
                    st.session_state.processing_results
                )
    
    def render_footer(self) -> None:
        """Render application footer"""
        AppStyles.render_footer()
    
    def run(self) -> None:
        """Main application entry point (Template Method Pattern)"""
        # Step 1: Configure page
        self.configure_page()
        
        # Step 2: Render header
        self.render_header()
        
        # Step 3: Handle configuration
        config = self.handle_configuration()
        
        # Step 4: Render input section (now includes processing button)
        audio_url, text_input = self.render_input_section()
        
        # Step 5: Render results
        self.render_results_section()
        
        # Step 6: Render footer
        self.render_footer()


# Application factory function
def create_app() -> MedicalAIApp:
    """Factory function to create and configure the application"""
    return MedicalAIApp()


# Main execution
if __name__ == "__main__":
    try:
        app = create_app()
        app.run()
        
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.exception(e)