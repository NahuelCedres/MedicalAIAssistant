# Firebase + Flask
import flask
from firebase_functions import https_fn
from firebase_functions.options import set_global_options
from firebase_admin import initialize_app

# Configuration
from config.app_config import AppConfig
from utils.logger import Logger

# Interfaces
from interfaces.audio_processor import AudioProcessorInterface
from interfaces.file_downloader import FileDownloaderInterface
from interfaces.response_formatter import ResponseFormatterInterface
from interfaces.medical_extractor import MedicalExtractorInterface
from interfaces.diagnosis_generator import DiagnosisGeneratorInterface, TreatmentRecommenderInterface

# Implementations
from services.openai_audio_processor import OpenAIAudioProcessor
from services.http_file_downloader import HTTPFileDownloader
from services.json_response_formatter import JSONResponseFormatter
from services.openai_medical_extractor import OpenAIMedicalExtractor
from services.openai_diagnosis_generator import OpenAIDiagnosisGenerator
from services.perplexity_treatment_recommender import PerplexityTreatmentRecommender

# Controllers and middleware
from controllers.audio_controller import AudioController
from controllers.medical_controller import MedicalController
from controllers.diagnosis_controller import DiagnosisController
from middleware.validation_middleware import ValidationMiddleware
from middleware.error_handler_middleware import ErrorHandlerMiddleware


# Modelos
from models.audio_models import AudioLinkInput
from models.medical_models import MedicalExtractionInput
from models.diagnosis_models import DiagnosisGenerationInput

#APIKEY
import os
from dotenv import load_dotenv
load_dotenv()

class DependencyContainer:
    """Dependency Injection"""
    
    def __init__(self, config: AppConfig):
        self.config = config
        self._audio_processor: AudioProcessorInterface = None
        self._file_downloader: FileDownloaderInterface = None
        self._response_formatter: ResponseFormatterInterface = None
        self._audio_controller: AudioController = None
        
        self._validation_middleware: ValidationMiddleware = None
        
        self._medical_extractor: MedicalExtractorInterface = None
        self._medical_controller: MedicalController = None
        
        self._diagnosis_controller: DiagnosisController = None
        self._treatment_recommender: TreatmentRecommenderInterface = None
        self._diagnosis_generator: DiagnosisGeneratorInterface = None
        
    @property
    def audio_processor(self) -> AudioProcessorInterface:
        if self._audio_processor is None:
            self._audio_processor = OpenAIAudioProcessor(
                api_key=self.config.openai_api_key
            )
        return self._audio_processor
        
    @property
    def file_downloader(self) -> FileDownloaderInterface:
        if self._file_downloader is None:
            self._file_downloader = HTTPFileDownloader(
                timeout=self.config.download_timeout
            )
        return self._file_downloader
    
    @property
    def response_formatter(self) -> ResponseFormatterInterface:
        if self._response_formatter is None:
            self._response_formatter = JSONResponseFormatter()
        return self._response_formatter
    
    @property
    def audio_controller(self) -> AudioController:
        if self._audio_controller is None:
            self._audio_controller = AudioController(
                self.audio_processor,
                self.file_downloader,
                self.response_formatter
            )
        return self._audio_controller
    
    @property
    def validation_middleware(self) -> ValidationMiddleware:
        if self._validation_middleware is None:
            self._validation_middleware = ValidationMiddleware(
                self.response_formatter
            )
        return self._validation_middleware

    @property
    def medical_extractor(self) -> MedicalExtractorInterface:
        if self._medical_extractor is None:
            self._medical_extractor = OpenAIMedicalExtractor(
                api_key=self.config.openai_api_key,
                model=self.config.medical_model
            )
        return self._medical_extractor
    
    @property
    def medical_controller(self) -> MedicalController:
        if self._medical_controller is None:
            self._medical_controller = MedicalController(
                self.medical_extractor,
                self.response_formatter
            )
        return self._medical_controller

    @property
    def diagnosis_generator(self) -> DiagnosisGeneratorInterface:
        if self._diagnosis_generator is None:
            self._diagnosis_generator = OpenAIDiagnosisGenerator(
                api_key=self.config.openai_api_key,
                model=self.config.medical_model
            )
        return self._diagnosis_generator
    
    @property
    def treatment_recommender(self) -> TreatmentRecommenderInterface:
        if self._treatment_recommender is None:
            self._treatment_recommender = PerplexityTreatmentRecommender(
                api_key=self.config.perplexity_api_key,
                model="sonar"  # Cambiar a modelo que funciona
            )
        return self._treatment_recommender
    
    @property
    def diagnosis_controller(self) -> DiagnosisController:
        if self._diagnosis_controller is None:
            self._diagnosis_controller = DiagnosisController(
                self.diagnosis_generator,
                self.treatment_recommender,
                self.response_formatter
            )
        return self._diagnosis_controller   

def create_app() -> flask.Flask:
    """Create Flask App"""
    
    # configuration
    config = AppConfig.from_environment()
    Logger.setup_logging(config.log_level)
    
    # Dependency containers
    container = DependencyContainer(config)
    
    # Create app
    app = flask.Flask(__name__)
    
    # Error Handler Middleware
    ErrorHandlerMiddleware(app, container.response_formatter)
    
    # endpoints
    @app.get("/")
    def home():
        return container.response_formatter.success_response({
           "message": "Medical AI Processing API",
            "version": "1.0.0",
            "description": "Audio transcription, medical information extraction, and diagnosis generation API",
            "endpoints": {
                "/health": "GET - API health status",
                "/transcribe-audio": "POST - Transcribe audio from URL using Whisper",
                "/extract-medical-info": "POST - Extract medical information from text using LLM",
                "/generate-diagnosis": "POST - Generate diagnosis and treatment plan from medical data"
            },
            "pipeline": {
                "step_1": "Audio Transcription - Convert audio to text",
                "step_2": "Medical Extraction - Extract structured medical data",
                "step_3": "Diagnosis Generation - Generate diagnosis and treatment recommendations"
            },
            "usage": {
                "audio_transcription": {
                    "endpoint": "/transcribe-audio",
                    "method": "POST",
                    "body": {"audio_url": "https://example.com/audio.wav",
                             "lenguage": "english"},
                    
                },
                "medical_extraction": {
                    "endpoint": "/extract-medical-info", 
                    "method": "POST",
                    "body": {"text": "Patient presents with chest pain..."}
                },
                "diagnosis_generation": {
                    "endpoint": "/generate-diagnosis",
                    "method": "POST", 
                    "body": {
                        "medical_info": {
                            "patient_info": {"name": "John Doe", "age": 45, "gender": "male", "identification_number": "445566"},
                            "symptoms": [ {
                                          "symptom": "crushing chest pain",
                                          "duration": "2 hours",
                                          "severity": "severe",
                                          "location": "substernal, radiating to left arm and jaw"
                                        },
                                        {
                                          "symptom": "..."
                                        }],
                            "reason_for_consultation": "chest pain evaluation",
                            "additional_notes": "History of hypertension and high cholester..."
                        },
                        "include_differential": True,
                        "max_diagnoses": 3
                    }
                }
            }
        })
    
    @app.get("/health")
    def health():
        return container.audio_controller.health_check()

    #Function 1
    @app.post("/audio-link")
    @container.validation_middleware.validate_json(AudioLinkInput)
    def audio_link():
        """Function 1: Convert audio URL to text transcription"""
        validated_data: AudioLinkInput = flask.g.validated_data
        return container.audio_controller.process_audio_from_link(validated_data)

    #Function 2
    @app.post("/extract-medical-info")
    @container.validation_middleware.validate_json(MedicalExtractionInput)
    def extract_medical_info():
        """Function 2: Extract structured medical information from free text"""
        validated_data: MedicalExtractionInput = flask.g.validated_data
        return container.medical_controller.extract_medical_info(validated_data)

    #Function 3
    @app.post("/generate-diagnosis")
    @container.validation_middleware.validate_json(DiagnosisGenerationInput)
    def generate_diagnosis():
        """Function 3: Generate ICD-10 diagnosis with evidence-based treatment plan"""
        validated_data: DiagnosisGenerationInput = flask.g.validated_data
        return container.diagnosis_controller.generate_complete_diagnosis(validated_data)
    
    return app

# Firebase Settings
config = AppConfig.from_environment()
set_global_options(max_instances=config.max_instances)
initialize_app()

# Create Flask app
app = create_app()

@https_fn.on_request(timeout_sec=540, memory=1024)
def api(req: https_fn.Request) -> https_fn.Response:
    """Firebase Functions + Flask"""
    try:
        with app.request_context(req.environ):
            response = app.full_dispatch_request()
            
            response_data = response.get_data()
            if isinstance(response_data, bytes):
                response_data = response_data.decode('utf-8')
            
            return https_fn.Response(
                response_data,
                status=response.status_code,
                headers=dict(response.headers)
            )
    except Exception as e:
        import json
        import logging
        
        logging.exception("Error Firebase Function")
        error_response = {
            "success": False,
            "error": {
                "message": "Internal Server Error",
                "code": "firebase_error"
            }
        }
        
        return https_fn.Response(
            json.dumps(error_response),
            status=500,
            headers={"Content-Type": "application/json"}
        )