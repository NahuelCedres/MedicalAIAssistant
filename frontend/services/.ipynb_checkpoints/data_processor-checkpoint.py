from typing import Dict, Any, List, Optional
from interfaces.api_client import APIClientInterface

class DataProcessor:
    """Servicio para procesar pipeline de datos (SRP)"""
    
    def __init__(self, api_client: APIClientInterface):
        self.api_client = api_client  # DIP: depende de interface, no implementación
    
    def process_full_pipeline(self, 
                            audio_url: Optional[str] = None, 
                            text_input: Optional[str] = None,
                            show_progress_callback=None) -> Dict[str, Any]:
        """
        Process full medical AI pipeline
        
        Args:
            audio_url: URL to audio file (optional)
            text_input: Direct text input (optional)
            show_progress_callback: Function to show progress updates
            
        Returns:
            Dict containing all processing results
        """
        results = {}
        current_text = text_input
        
        try:
            # Step 1: Transcription (if audio provided)
            if audio_url:
                if show_progress_callback:
                    show_progress_callback("Step 1/3: Transcribing audio...")
                
                transcription_result = self.api_client.transcribe_audio(audio_url)
                
                if not transcription_result.get('success', False):
                    return {
                        'success': False,
                        'error': transcription_result.get('error', 'Transcription failed'),
                        'step_failed': 'transcription'
                    }
                
                current_text = transcription_result.get('result', {}).get('transcription', '')
                results['transcription'] = transcription_result
            
            # Step 2: Medical Information Extraction
            if current_text:
                if show_progress_callback:
                    show_progress_callback("Step 2/3: Extracting medical information...")
                
                extraction_result = self.api_client.extract_medical_info(current_text)
                
                if not extraction_result.get('success', False):
                    return {
                        'success': False,
                        'error': extraction_result.get('error', 'Medical extraction failed'),
                        'step_failed': 'extraction',
                        'partial_results': results
                    }
                
                results['extraction'] = extraction_result
            
            # Step 3: Diagnosis Generation
            if 'extraction' in results:
                if show_progress_callback:
                    show_progress_callback("Step 3/3: Generating diagnosis...")
                
                # Format data for diagnosis API (match expected structure)
                diagnosis_payload = {
                    "medical_info": results['extraction']['result'],
                    "include_differential": True,
                    "max_diagnoses": 3
                }
                
                diagnosis_result = self.api_client.generate_diagnosis(diagnosis_payload)
                
                if not diagnosis_result.get('success', False):
                    return {
                        'success': False,
                        'error': diagnosis_result.get('error', 'Diagnosis generation failed'),
                        'step_failed': 'diagnosis',
                        'partial_results': results
                    }
                
                results['diagnosis'] = diagnosis_result
            
            return {
                'success': True,
                'results': results
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Unexpected error in pipeline: {str(e)}",
                'partial_results': results
            }
    
    def process_single_step(self, 
                          step: str, 
                          input_data: Any) -> Dict[str, Any]:
        """Process a single step of the pipeline (OCP)"""
        try:
            if step == 'transcription':
                return self.api_client.transcribe_audio(input_data)
            elif step == 'extraction':
                return self.api_client.extract_medical_info(input_data)
            elif step == 'diagnosis':
                # If input_data doesn't have the wrapper, add it
                if isinstance(input_data, dict) and 'medical_info' not in input_data:
                    diagnosis_payload = {
                        "medical_info": input_data,
                        "include_differential": True,
                        "max_diagnoses": 3
                    }
                    return self.api_client.generate_diagnosis(diagnosis_payload)
                else:
                    return self.api_client.generate_diagnosis(input_data)
            else:
                return {
                    'success': False,
                    'error': f"Unknown step: {step}"
                }
        except Exception as e:
            return {
                'success': False,
                'error': f"Error in {step}: {str(e)}"
            }