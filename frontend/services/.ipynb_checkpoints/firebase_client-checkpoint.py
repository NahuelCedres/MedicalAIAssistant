import requests
from typing import Dict, Any, Optional
from interfaces.api_client import APIClientInterface

class FirebaseAPIClient(APIClientInterface):
    """Implementación concreta para Firebase Functions (SRP)"""
    
    def __init__(self, timeout: int = 120):
        self.timeout = timeout
        self.endpoints = {
            'transcription': '',
            'extraction': '',
            'diagnosis': ''
        }
    
    def set_endpoint(self, service: str, url: str) -> None:
        """Set endpoint URL for specific service (OCP)"""
        if service in self.endpoints:
            self.endpoints[service] = url
        else:
            raise ValueError(f"Unknown service: {service}")
    
    def transcribe_audio(self, audio_url: str) -> Dict[str, Any]:
        """Transcribe audio using Firebase Function"""
        try:
            response = requests.post(
                self.endpoints['transcription'],
                json={"audio_url": audio_url},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Transcription API error: {str(e)}",
                "result": None
            }
    
    def extract_medical_info(self, text: str) -> Dict[str, Any]:
        """Extract medical information using Firebase Function"""
        try:
            response = requests.post(
                self.endpoints['extraction'],
                json={"text": text},
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Medical extraction API error: {str(e)}",
                "result": None
            }
    
    def generate_diagnosis(self, medical_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate diagnosis using Firebase Function"""
        try:
            response = requests.post(
                self.endpoints['diagnosis'],
                json=medical_data,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Diagnosis API error: {str(e)}",
                "result": None
            }
