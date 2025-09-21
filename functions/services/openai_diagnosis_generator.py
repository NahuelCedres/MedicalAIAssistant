import requests
import json
import logging
from typing import List
from interfaces.diagnosis_generator import DiagnosisGeneratorInterface
from models.diagnosis_models import Diagnosis, ICDCode
from models.medical_models import MedicalExtractionResult

class OpenAIDiagnosisGenerator(DiagnosisGeneratorInterface):
    """Diagnosis generator using GPT-4 with ICD-10 coding"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.logger = logging.getLogger(__name__)
    
    def generate_diagnosis_with_icd10(self, medical_info: MedicalExtractionResult, 
                                     max_diagnoses: int = 3) -> List[Diagnosis]:
        """Generate diagnoses with ICD-10 codes using GPT-4"""
        
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")
        
        try:
            self.logger.info("Generating diagnoses with ICD-10 codes using GPT-4")
            
            # Create structured prompt for diagnosis
            prompt = self._create_diagnosis_prompt(medical_info, max_diagnoses)
            
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
                            "content": "You are an experienced physician with expertise in ICD-10 coding. Analyze medical information and provide accurate diagnoses with proper ICD-10 codes. Always respond with valid JSON only."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.2,  
                    "max_tokens": 2000
                },
                timeout=45
            )
            
            self.logger.info(f"OpenAI diagnosis API response status: {response.status_code}")
            
            if response.status_code != 200:
                self.logger.error(f"OpenAI API Error: {response.status_code}")
                self.logger.error(f"Response content: {response.text}")
                response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Parse JSON response
            try:
                diagnosis_data = json.loads(content)
            except json.JSONDecodeError as e:
                self.logger.error(f"Error parsing diagnosis JSON response: {content}")
                raise ValueError(f"GPT returned invalid JSON: {str(e)}")
            
            # Convert to Pydantic models
            diagnoses = []
            for diag_data in diagnosis_data.get("diagnoses", []):
                icd_data = diag_data.get("icd_10_code", {})
                icd_code = ICDCode(
                    code=icd_data.get("code", ""),
                    description=icd_data.get("description", ""),
                    category=icd_data.get("category", "")
                )
                
                diagnosis = Diagnosis(
                    diagnosis_name=diag_data.get("diagnosis_name", ""),
                    icd_10_code=icd_code,
                    confidence_score=float(diag_data.get("confidence_score", 0.5)),
                    reasoning=diag_data.get("reasoning", ""),
                    supporting_symptoms=diag_data.get("supporting_symptoms", [])
                )
                diagnoses.append(diagnosis)
            
            self.logger.info(f"Generated {len(diagnoses)} diagnoses with ICD-10 codes")
            return diagnoses
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error in OpenAI diagnosis request: {str(e)}")
            raise ValueError(f"Error communicating with OpenAI API: {str(e)}")
        
        except Exception as e:
            self.logger.error(f"Error generating diagnoses: {str(e)}")
            raise ValueError(f"Error in diagnosis generation: {str(e)}")
    
    def _create_diagnosis_prompt(self, medical_info: MedicalExtractionResult, max_diagnoses: int) -> str:
        """Create prompt for diagnosis generation with ICD-10"""
        
        # Format patient info
        patient = medical_info.patient_info
        patient_summary = f"Patient: {patient.name or 'Unknown'}, Age: {patient.age or 'Unknown'}, Gender: {patient.gender or 'Unknown'}"
        
        # Format symptoms
        symptoms_list = []
        for symptom in medical_info.symptoms:
            symptom_desc = symptom.symptom
            if symptom.duration:
                symptom_desc += f" (duration: {symptom.duration})"
            if symptom.severity:
                symptom_desc += f" (severity: {symptom.severity})"
            if symptom.location:
                symptom_desc += f" (location: {symptom.location})"
            symptoms_list.append(symptom_desc)
        
        symptoms_text = "\n".join([f"- {s}" for s in symptoms_list])
        
        return f"""
Based on the following medical information, provide {max_diagnoses} most likely diagnoses with proper ICD-10 codes.

{patient_summary}

Reason for consultation: {medical_info.reason_for_consultation}

Symptoms:
{symptoms_text}

{f"Additional notes: {medical_info.additional_notes}" if medical_info.additional_notes else ""}

Provide a JSON response with exactly this structure:

{{
    "diagnoses": [
        {{
            "diagnosis_name": "Primary diagnosis name",
            "icd_10_code": {{
                "code": "ICD-10 code (e.g., G43.1)",
                "description": "Full ICD-10 description",
                "category": "ICD-10 category (e.g., Diseases of the nervous system)"
            }},
            "confidence_score": 0.85,
            "reasoning": "Clinical reasoning explaining why this diagnosis fits the symptoms",
            "supporting_symptoms": ["symptom1", "symptom2", "symptom3"]
        }}
    ]
}}

Order diagnoses by likelihood (most probable first). Include proper ICD-10 codes and clinical reasoning.
Respond ONLY with valid JSON:
"""
    
    def is_ready(self) -> bool:
        """Check if diagnosis generator is ready"""
        return bool(self.api_key)