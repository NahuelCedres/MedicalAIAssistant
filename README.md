# Medical AI Processing System

A comprehensive medical AI system that processes audio consultations through a 3-step pipeline: audio transcription, medical information extraction, and diagnosis generation with treatment recommendations.

## System Overview

This system implements a complete medical AI workflow:

1. **Audio Transcription**: Convert medical consultation audio to text using OpenAI Whisper
2. **Medical Information Extraction**: Extract structured medical data using GPT-4
3. **Diagnosis Generation**: Generate diagnosis and treatment plans using Perplexity AI with current medical guidelines

## Architecture

The system follows SOLID principles with clean architecture:

- **Backend**: Flask API with dependency injection and interface-based design
- **Frontend**: Streamlit application with modular components
- **Database**: Stateless design with external AI service integration

### Key Design Principles

- **Single Responsibility**: Each service has one clear purpose
- **Open/Closed**: Extensible through interfaces without modifying existing code
- **Liskov Substitution**: Interchangeable implementations via interfaces
- **Interface Segregation**: Specific, focused interfaces
- **Dependency Inversion**: Dependency injection container with interface-based dependencies

## Project Structure

```
MedicalAIAssistant/
├── functions/                         # Backend (Firebase Functions)
│   ├── config/
│   │   └── app_config.py              # Centralized configuration
│   ├── controllers/
│   │   ├── audio_controller.py        # Audio processing endpoints
│   │   ├── diagnosis_controller.py    # Diagnosis generation endpoints
│   │   └── medical_controller.py      # Medical extraction endpoints
│   ├── interfaces/
│   │   ├── audio_processor.py         # Audio processing interface
│   │   ├── file_downloader.py         # File download interface
│   │   ├── diagnosis_generator.py     # Diagnosis generation interface
│   │   ├── medical_extractor.py       # Medical extraction interface
│   │   └── response_formatter.py      # Response formatting interface
│   ├── middleware/
│   │   ├── error_handler_middleware.py # Global error handling
│   │   └── validation_middleware.py   # Request validation
│   ├── models/
│   │   ├── audio_models.py            # Audio processing models
│   │   ├── diagnosis_models.py        # Diagnosis generation models
│   │   └── medical_models.py          # Medical data models
│   ├── services/
│   │   ├── http_file_downloader.py    # HTTP file download service
│   │   ├── openai_audio_processor.py  # OpenAI Whisper integration
│   │   ├── json_response_formatter.py # JSON response formatter
│   │   ├── openai_diagnosis_generator.py # Perplexity AI diagnosis generation
│   │   └── openai_medical_extractor.py # GPT-4 medical extraction
│   ├── utils/
│   │   └── logger.py                  # Logging utilities
│   ├── main.py                        # Application entry point
│   ├── .env                           # Environment variables
│   └── requirements.txt               # Backend dependencies
├── frontend/                          # Frontend (Streamlit)
│   ├── components/
│   │   ├── __init__.py                # Package initialization
│   │   ├── audio_input.py             # Audio upload component
│   │   ├── text_input.py              # Text input component
│   │   ├── results_display.py         # Results visualization
│   │   └── configuration.py           # Configuration component
│   ├── interfaces/
│   │   ├── __init__.py                # Package initialization
│   │   ├── api_client.py              # API client interface
│   │   ├── result_formatter.py        # Result formatting interface
│   │   └── ui_component.py            # UI component interface
│   ├── services/
│   │   ├── __init__.py                # Package initialization
│   │   ├── firebase_client.py         # Firebase API client
│   │   └── data_processor.py          # Data processing service
│   ├── utils/
│   │   ├── __init__.py                # Package initialization
│   │   ├── formatters.py              # Result formatters
│   │   └── styles.py                  # CSS styling
│   ├── app.py                         # Main Streamlit application
│   └── requirements.txt               # Frontend dependencies
├── firebase.json                      # Firebase configuration
├── .firebaserc                        # Firebase project configuration
├── .gitignore                         # Git ignore file
└── README.md                          # Project documentation
```

## Features

### Backend API

- **Audio Transcription Endpoint**: `/transcribe-audio`
  - Accepts audio URLs
  - Supports multiple audio formats
  - Language detection and specification
  - Returns structured transcription results

- **Medical Information Extraction**: `/extract-medical-info`
  - Processes medical consultation text
  - Extracts patient information, symptoms, consultation reasons
  - Returns structured medical data

- **Diagnosis Generation**: `/generate-diagnosis`
  - Generates primary and differential diagnoses
  - Provides ICD-10 codes
  - Creates detailed treatment plans
  - Includes evidence-based citations

### Frontend Application

- **Intuitive Interface**: Clean, medical-professional design
- **Multiple Input Methods**: Audio URL or direct text input
- **Real-time Processing**: Visual feedback during processing
- **Comprehensive Results**: Organized display of all processing results
- **Responsive Design**: Works on desktop and mobile devices

## API Documentation

### Authentication

Currently, the system uses API keys for external services. In production, implement proper authentication middleware.

### Endpoints

#### GET `/`
Returns API documentation and available endpoints.

**Response:**
```json
{
  "success": true,
  "result": {
    "message": "Medical AI Processing API",
    "version": "1.0.0",
    "endpoints": { ... }
  }
}
```

#### POST `/transcribe-audio`
Transcribe audio from URL.

**Request:**
```json
{
  "audio_url": "https://example.com/audio.wav",
  "language": "english",
  "max_duration": 300
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "transcription": "Patient presents with...",
    "duration_seconds": 45.2,
    "language_detected": "english",
    "model_used": "openai-whisper-1"
  },
  "metadata": {
    "processing_time_seconds": 12.5,
    "timestamp": "2025-09-21T19:30:00Z"
  }
}
```

#### POST `/extract-medical-info`
Extract medical information from text.

**Request:**
```json
{
  "text": "Patient John Smith, 45 years old, presents with severe chest pain..."
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "patient_info": {
      "name": "Robert Davis",
      "age": 58,
      "gender": "Male",
      "identification_number": "445566"
    },
    "symptoms": [
      {
        "symptom": "Crushing chest pain",
        "duration": "2 hours",
        "severity": "Severe",
        "location": "Substernal, radiating to left arm and jaw"
      },
      {
        "symptom": "Shortness of breath",
        "duration": "2 hours",
        "severity": "Severe",
        "location": null
      },
      {
        "symptom": "Diaphoresis",
        "duration": "2 hours",
        "severity": "Severe",
        "location": null
      },
      {
        "symptom": "Nausea",
        "duration": "2 hours",
        "severity": "Severe",
        "location": null
      }
    ],
    "reason_for_consultation": "Crushing chest pain, shortness of breath, diaphoresis, and nausea",
    "additional_notes": "Patient has a history of hypertension and high cholesterol. Denies recent illness or trauma."
  },
  "metadata": {
    "processing_time_seconds": 7.53,
    "symptoms_found": 4,
    "text_length": 455,
    "timestamp": "2025-09-21T20:50:44.032858+00:00"
  }
}
```

#### POST `/generate-diagnosis`
Generate diagnosis and treatment plan.

**Request:**
```json
{
  "medical_info": {
    "patient_info": { ... },
    "symptoms": [ ... ],
    "reason_for_consultation": "chest pain evaluation"
  },
  "include_differential": true,
  "max_diagnoses": 3
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "primary_diagnosis": {
      "diagnosis_name": "Acute Myocardial Infarction",
      "confidence_score": 0.95,
      "icd_10_code": {
        "code": "I21.9",
        "category": "Diseases of the circulatory system",
        "description": "Acute myocardial infarction, unspecified"
      },
      "reasoning": "The patient's symptoms of severe, crushing chest pain radiating to the left arm and jaw, severe shortness of breath, diaphoresis, and nausea are classic symptoms of an acute myocardial infarction.",
      "supporting_symptoms": [
        "crushing chest pain",
        "shortness of breath",
        "diaphoresis",
        "nausea"
      ]
    },
    "differential_diagnoses": [
      {
        "diagnosis_name": "Unstable Angina",
        "confidence_score": 0.85,
        "icd_10_code": {
          "code": "I20.0",
          "category": "Diseases of the circulatory system",
          "description": "Unstable angina"
        },
        "reasoning": "The patient's symptoms could also be indicative of unstable angina, characterized by chest pain due to insufficient blood flow to the heart.",
        "supporting_symptoms": [
          "crushing chest pain",
          "shortness of breath",
          "diaphoresis",
          "nausea"
        ]
      }
    ],
    "treatment_plan": [
      {
        "category": "clinical",
        "priority": "high",
        "recommendation": "Perform immediate clinical assessment including history, physical exam, 12-lead ECG within 10 minutes of presentation, and cardiac biomarkers (troponin) to confirm diagnosis of acute myocardial infarction (AMI).",
        "duration": "initial assessment on presentation",
        "notes": "2025 ACC/AHA/ESC guidelines emphasize rapid diagnosis to differentiate STEMI vs NSTEMI and initiate timely treatment[3][4][6]."
      },
      {
        "category": "clinical",
        "priority": "high",
        "recommendation": "Administer aspirin 160-325 mg orally immediately unless contraindicated, plus initiate P2Y12 inhibitor (e.g., ticagrelor 180 mg loading dose) for dual antiplatelet therapy.",
        "duration": "continue dual antiplatelet therapy for at least 12 months",
        "notes": "Class 1 recommendation in 2025 ACC/AHA and ESC guidelines for all type 1 MI patients to reduce thrombotic events[3][6]."
      }
    ],
    "evidence_citations": [
      "https://www.heartfoundation.org.au/for-professionals/acs-guideline",
      "https://consultqd.clevelandclinic.org/new-guideline-on-acute-coronary-syndromes-key-takeaways-for-cardiologists",
      "https://professional.heart.org/en/guidelines-statements/2025-accahaacepnaemspscai-guideline-for-the-management-of-patients-with-acutecir0000000000001309",
      "https://pubmed.ncbi.nlm.nih.gov/40014670/",
      "https://www.acc.org/Guidelines",
      "https://www.escardio.org/Guidelines/Clinical-Practice-Guidelines/Acute-Coronary-Syndromes-ACS-Guidelines"
    ]
  },
  "metadata": {
    "processing_time_seconds": 31.02,
    "primary_diagnosis_confidence": 0.95,
    "diagnoses_generated": 3,
    "treatment_recommendations": 10,
    "evidence_citations": 6,
    "icd_10_code": "I21.9",
    "timestamp": "2025-09-21T19:56:29.188809+00:00"
  }
}
```

## Installation & Setup

### Prerequisites

- Python 3.8+
- Node.js 16+ (for frontend development)
- OpenAI API key
- Perplexity API key
- Firebase project (for deployment)

### Backend Setup

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/medical-ai-system.git
cd medical-ai-system/backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
export OPENAI_API_KEY="your-openai-key"
export PERPLEXITY_API_KEY="your-perplexity-key"
export LOG_LEVEL="INFO"
```


### Firebase Deployment

1. **Install Firebase CLI:**
```bash
npm install -g firebase-tools
```

2. **Initialize Firebase project:**
```bash
firebase init functions
```

3. **Deploy functions:**
```bash
firebase deploy --only functions
```

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd ../frontend
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure API endpoints:**
Update the URLs in the Streamlit sidebar to point to your backend API.

4. **Run the frontend:**
```bash
streamlit run app.py
```

The frontend will be available at `http://localhost:8501`


## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for Whisper and GPT-4 | Required |
| `PERPLEXITY_API_KEY` | Perplexity API key for diagnosis generation | Required |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | INFO |
| `MAX_FILE_SIZE_MB` | Maximum audio file size | 50 |
| `MAX_AUDIO_DURATION` | Maximum audio duration in seconds | 300 |
| `DOWNLOAD_TIMEOUT` | File download timeout in seconds | 30 |

### API Configuration

The system supports configuration through environment variables or the `AppConfig` class:

```python
config = AppConfig.from_environment()
```

## Monitoring & Logging

The system includes comprehensive logging:

- **Request/Response logging**: All API calls are logged
- **Error tracking**: Detailed error information with stack traces
- **Performance metrics**: Processing times for each step
- **Health checks**: Service availability monitoring

## Security Considerations

- **API Key Management**: Store API keys securely using environment variables
- **Input Validation**: All inputs are validated using Pydantic models
- **File Size Limits**: Prevent abuse with configurable file size limits
- **Error Handling**: Sanitized error responses to prevent information leakage
- **HTTPS**: Use HTTPS in production environments

## Performance Optimization

- **Caching**: Implement caching for repeated requests
- **Async Processing**: Consider async processing for large files
- **Rate Limiting**: Implement rate limiting for production use
- **Load Balancing**: Use load balancers for high availability




## Disclaimer

This system is for demonstration and educational purposes only. It should not be used for actual medical diagnosis or treatment decisions. Always consult qualified healthcare professionals for medical advice.
