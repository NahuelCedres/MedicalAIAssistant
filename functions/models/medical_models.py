from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

class MedicalExtractionInput(BaseModel):
    """Input for medical information extraction"""
    text: str = Field(..., min_length=10, description="Medical text to process")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Patient John Smith, 45 years old, ID 12345. Consulting for severe headache for 3 days, accompanied by nausea and light sensitivity."
            }
        }

class PatientInfo(BaseModel):
    """Patient information"""
    name: Optional[str] = Field(None, description="Patient name")
    age: Optional[int] = Field(None, ge=0, le=150, description="Patient age")
    identification_number: Optional[str] = Field(None, description="Patient identification number")
    gender: Optional[str] = Field(None, description="Patient gender")
    
class Symptom(BaseModel):
    """Symptom information"""
    symptom: str = Field(..., description="Symptom description")
    duration: Optional[str] = Field(None, description="Symptom duration")
    severity: Optional[str] = Field(None, description="Severity (mild, moderate, severe)")
    location: Optional[str] = Field(None, description="Symptom location")

class MedicalExtractionResult(BaseModel):
    """Medical extraction results"""
    patient_info: PatientInfo
    symptoms: List[Symptom]
    reason_for_consultation: str = Field(..., description="Main reason for consultation")
    additional_notes: Optional[str] = Field(None, description="Additional notes")
    
class MedicalExtractionResponse(BaseModel):
    """Complete medical extraction response"""
    success: bool
    result: Optional[MedicalExtractionResult] = None
    error: Optional[str] = None
    metadata: Optional[dict] = None