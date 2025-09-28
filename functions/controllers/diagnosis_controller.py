import time
import logging
from typing import Optional
import flask
from models.diagnosis_models import DiagnosisGenerationInput, DiagnosisGenerationResult
from interfaces.diagnosis_generator import DiagnosisGeneratorInterface, TreatmentRecommenderInterface
from interfaces.response_formatter import ResponseFormatterInterface

class DiagnosisController:
    """Controller for diagnosis generation with ICD-10 and treatment recommendations"""
    
    def __init__(self, 
                 diagnosis_generator: DiagnosisGeneratorInterface,
                 treatment_recommender: TreatmentRecommenderInterface,
                 response_formatter: ResponseFormatterInterface):
        self.diagnosis_generator = diagnosis_generator
        self.treatment_recommender = treatment_recommender
        self.response_formatter = response_formatter
        self.logger = logging.getLogger(__name__)
    
    def generate_complete_diagnosis(self, input_data: DiagnosisGenerationInput) -> flask.Response:
        """Generate complete diagnosis with ICD-10 codes and treatment recommendations"""
        start_time = time.time()
        
        try:
            self.logger.info("Starting complete diagnosis generation process")
            
            # Step 1: Generate diagnoses with ICD-10 codes using GPT-4
            self.logger.info("Generating diagnoses with ICD-10 codes")
            diagnoses = self.diagnosis_generator.generate_diagnosis_with_icd10(
                input_data.medical_info, 
                input_data.max_diagnoses
            )
            
            if not diagnoses:
                raise ValueError("No diagnoses could be generated from the provided medical information")
            
            # Primary diagnosis is the first 
            primary_diagnosis = diagnoses[0]
            differential_diagnoses = diagnoses[1:] if input_data.include_differential else []
            
            self.logger.info(f"Generated primary diagnosis: {primary_diagnosis.diagnosis_name} ({primary_diagnosis.icd_10_code.code})")
            
            # Step 2: Get treatment recommendations using Perplexity
            self.logger.info("Getting treatment recommendations from Perplexity")
            patient_age = input_data.medical_info.patient_info.age or None
            patient_gender = input_data.medical_info.patient_info.gender
            
            treatment_recommendations, citations = self.treatment_recommender.get_treatment_recommendations(
                primary_diagnosis,
                patient_age,
                patient_gender
            )
            
            # Create complete result
            result = DiagnosisGenerationResult(
                primary_diagnosis=primary_diagnosis,
                differential_diagnoses=differential_diagnoses,
                treatment_plan=treatment_recommendations,
                evidence_citations=citations
            )
            
            # Metadata
            metadata = {
                "processing_time_seconds": round(time.time() - start_time, 2),
                "diagnoses_generated": len(diagnoses),
                "treatment_recommendations": len(treatment_recommendations),
                "evidence_citations": len(citations),
                "primary_diagnosis_confidence": primary_diagnosis.confidence_score,
                "icd_10_code": primary_diagnosis.icd_10_code.code
            }
            
            self.logger.info("Complete diagnosis generation completed successfully")
            return self.response_formatter.success_response(
                result.dict(), 
                metadata
            )
            
        except ValueError as e:
            self.logger.error(f"Validation error in diagnosis generation: {str(e)}")
            return self.response_formatter.error_response(
                str(e), 
                status_code=400,
                error_code="validation_error"
            )
            
        except Exception as e:
            self.logger.error(f"Internal error in diagnosis generation: {str(e)}")
            return self.response_formatter.error_response(
                "Internal server error during diagnosis generation",
                status_code=500,
                error_code="internal_error"
            )