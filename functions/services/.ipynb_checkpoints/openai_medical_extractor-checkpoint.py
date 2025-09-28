import requests
import json
import logging
from typing import Dict, Any
from interfaces.medical_extractor import MedicalExtractorInterface
from models.medical_models import MedicalExtractionResult, PatientInfo, Symptom

class OpenAIMedicalExtractor(MedicalExtractorInterface):
    """Medical information extractor using OpenAI"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.logger = logging.getLogger(__name__)
    
    def extract_medical_info(self, text: str) -> MedicalExtractionResult:
        """Extract medical information from text using GPT"""
        
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")
        
        try:
            self.logger.info("Extracting medical information...")
            
            # Crear prompt
            prompt = self._create_extraction_prompt(text)
            
            # Request to OpenAI
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a medical assistant specialized in extracting structured information from medical texts. Respond ONLY with valid JSON following exactly the provided schema."
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ],
                    "temperature": 0.1,  
                    "max_tokens": 1000
                },
                timeout=30
            )
            
            self.logger.info(f"OpenAI API response status: {response.status_code}")
            
            if response.status_code != 200:
                self.logger.error(f"OpenAI API Error: {response.status_code}")
                self.logger.error(f"Response content: {response.text}")
                response.raise_for_status()
            
            # Parse response
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Parse JSON from response
            try:
                extracted_data = json.loads(content)
            except json.JSONDecodeError as e:
                self.logger.error(f"Error parsing JSON response: {content}")
                raise ValueError(f"GPT returned invalid JSON: {str(e)}")
            
            # Convert to Pydantic model
            return self._parse_extraction_result(extracted_data)
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error in request to OpenAI: {str(e)}")
            raise ValueError(f"Error communicating with OpenAI API: {str(e)}")
        
        except Exception as e:
            self.logger.error(f"Error extracting medical information: {str(e)}")
            raise ValueError(f"Error in extraction: {str(e)}")
    
    def _create_extraction_prompt(self, text: str) -> str:
        """Create prompt for medical extraction"""
        return f"""
Extract medical information from the following text and return a JSON with exactly this structure:

{{
    "patient_info": {{
        "name": "patient name or null",
        "age": age_number or null,
        "identification_number": "ID or null", 
        "gender": "gender or null"
    }},
    "symptoms": [
        {{
            "symptom": "symptom description",
            "duration": "duration or null",
            "severity": "mild/moderate/severe or null",
            "location": "location or null"
        }}
    ],
    "reason_for_consultation": "main reason for consultation",
    "additional_notes": "additional notes or null"
}}

Medical text:
{text}

Respond ONLY with valid JSON, no additional explanations:
"""
    
    def _parse_extraction_result(self, data: Dict[str, Any]) -> MedicalExtractionResult:
        """Parse extraction result to Pydantic models"""
        
        # 1- Parse patient information
        patient_data = data.get("patient_info", {})
        patient_info = PatientInfo(
            name=patient_data.get("name"),
            age=patient_data.get("age"),
            identification_number=patient_data.get("identification_number"),
            gender=patient_data.get("gender")
        )
        
        # 2- Parse symptoms
        symptoms = []
        for symptom_data in data.get("symptoms", []):
            symptom = Symptom(
                symptom=symptom_data.get("symptom", ""),
                duration=symptom_data.get("duration"),
                severity=symptom_data.get("severity"),
                location=symptom_data.get("location")
            )
            symptoms.append(symptom)
        
       # Create final result
        return MedicalExtractionResult(
            patient_info=patient_info,
            symptoms=symptoms,
            reason_for_consultation=data.get("reason_for_consultation", ""),
            additional_notes=data.get("additional_notes")
        )
    
    def is_ready(self) -> bool:
        """Check if the extractor is ready"""
        return bool(self.api_key)