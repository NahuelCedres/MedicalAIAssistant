from abc import ABC, abstractmethod
from typing import List
from models.diagnosis_models import DiagnosisGenerationResult, Diagnosis, TreatmentRecommendation
from models.medical_models import MedicalExtractionResult

class DiagnosisGeneratorInterface(ABC):
    """Interface for diagnosis generators"""
    
    @abstractmethod
    def generate_diagnosis_with_icd10(self, medical_info: MedicalExtractionResult, 
                                     max_diagnoses: int = 3) -> List[Diagnosis]:
        """Generate diagnoses with ICD-10 codes"""
        pass
    
    @abstractmethod
    def is_ready(self) -> bool:
        """Check if diagnosis generator is ready"""
        pass

class TreatmentRecommenderInterface(ABC):
    """Interface for treatment recommenders"""
    
    @abstractmethod
    def get_treatment_recommendations(self, diagnosis: Diagnosis, 
                                    patient_age: int, 
                                    patient_gender: str = None) -> tuple[List[TreatmentRecommendation], List[str]]:
        """Get treatment recommendations for a diagnosis with citations"""
        pass
    
    @abstractmethod
    def is_ready(self) -> bool:
        """Check if treatment recommender is ready"""
        pass