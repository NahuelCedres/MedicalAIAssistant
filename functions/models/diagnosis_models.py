from pydantic import BaseModel, Field, validator
from typing import List, Optional
from models.medical_models import MedicalExtractionResult

class DiagnosisGenerationInput(BaseModel):
    """Input for diagnosis generation from medical extraction result"""
    medical_info: MedicalExtractionResult = Field(..., description="Extracted medical information")
    include_differential: bool = Field(True, description="Include differential diagnoses")
    max_diagnoses: int = Field(3, ge=1, le=5, description="Maximum number of diagnoses to generate")
    
    class Config:
        json_schema_extra = {
            "example": {
                "medical_info": {
                    "patient_info": {
                        "name": "John Smith",
                        "age": 45,
                        "gender": "male"
                    },
                    "symptoms": [
                        {
                            "symptom": "severe headache",
                            "duration": "3 days",
                            "severity": "severe"
                        }
                    ],
                    "reason_for_consultation": "severe headache"
                },
                "include_differential": True,
                "max_diagnoses": 3
            }
        }

class ICDCode(BaseModel):
    """ICD-10 code with description"""
    code: str = Field(..., description="ICD-10 code")
    description: str = Field(..., description="ICD-10 description")
    category: str = Field(..., description="ICD-10 category")

class Diagnosis(BaseModel):
    """Individual diagnosis with ICD-10 coding"""
    diagnosis_name: str = Field(..., description="Primary diagnosis name")
    icd_10_code: ICDCode = Field(..., description="ICD-10 coding")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score 0-1")
    reasoning: str = Field(..., description="Clinical reasoning for diagnosis")
    supporting_symptoms: List[str] = Field(..., description="Symptoms supporting this diagnosis")

class TreatmentRecommendation(BaseModel):
    """Treatment recommendation from Perplexity"""
    category: str = Field(..., description="Treatment category (medication, lifestyle, procedure, monitoring, education, red_flags, follow_up)")
    recommendation: str = Field(..., description="Specific treatment recommendation")
    priority: str = Field(..., description="Priority level (high, medium, low)")
    duration: Optional[str] = Field(None, description="Recommended duration")
    notes: Optional[str] = Field(None, description="Additional notes or contraindications")

class DiagnosisGenerationResult(BaseModel):
    """Complete diagnosis generation result"""
    primary_diagnosis: Diagnosis = Field(..., description="Most likely diagnosis")
    differential_diagnoses: List[Diagnosis] = Field(default=[], description="Alternative diagnoses")
    treatment_plan: List[TreatmentRecommendation] = Field(..., description="Complete treatment plan including red flags and follow-up")
    evidence_citations: List[str] = Field(default=[], description="Citations from medical literature used for treatment recommendations")
    
class DiagnosisGenerationResponse(BaseModel):
    """Complete response for diagnosis generation"""
    success: bool
    result: Optional[DiagnosisGenerationResult] = None
    error: Optional[str] = None
    metadata: Optional[dict] = None