import requests
import json
import logging
from typing import List
from interfaces.diagnosis_generator import TreatmentRecommenderInterface
from models.diagnosis_models import Diagnosis, TreatmentRecommendation

class PerplexityTreatmentRecommender(TreatmentRecommenderInterface):
    """Treatment recommender using Perplexity AI"""
    
    def __init__(self, api_key: str, model: str = "sonar"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.logger = logging.getLogger(__name__)
    
    def get_treatment_recommendations(self, diagnosis: Diagnosis, 
                                    patient_age: int, 
                                    patient_gender: str = None) -> tuple[List[TreatmentRecommendation], List[str]]:
        """Get evidence-based treatment recommendations using Perplexity with citations"""
        
        if not self.api_key:
            raise ValueError("Perplexity API key not configured")
        
        try:
            self.logger.info(f"Getting treatment recommendations for {diagnosis.diagnosis_name} using Perplexity")
            
            #Create treatment query prompt
            prompt = self._create_treatment_prompt(diagnosis, patient_age, patient_gender)
            
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
                            "content": "You are a medical AI that provides evidence-based clinical pathways in JSON format. Always respond with valid JSON structure only. Never include explanations outside the JSON."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.0, 
                    "max_tokens": 4000
                },
                timeout=45
            )
            
            self.logger.info(f"Perplexity API response status: {response.status_code}")
            
            if response.status_code != 200:
                self.logger.error(f"Perplexity API Error: {response.status_code}")
                self.logger.error(f"Response content: {response.text}")
                response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            #Log the raw content for debugging
            self.logger.info(f"Perplexity pathway response: {content[:200]}...")
            
            #Extract citations from response
            citations = result.get("citations", [])
            self.logger.info(f"Extracted {len(citations)} citations from Perplexity response")
            
            #Extract JSON from response 
            json_content = self._extract_json_from_response(content)
            
            #Try to parse as JSON
            try:
                pathway_data = json.loads(json_content)
                recommendations = []
                
                for rec_data in pathway_data.get("clinical_pathway", []):
                    recommendation = TreatmentRecommendation(
                        category="clinical",
                        recommendation=rec_data.get("recommendation", ""),
                        priority=rec_data.get("priority", "medium"),
                        duration=rec_data.get("duration"),
                        notes=rec_data.get("notes", "Based on clinical guidelines")
                    )
                    recommendations.append(recommendation)
                
                self.logger.info(f"Parsed {len(recommendations)} recommendations from JSON response")
                return recommendations, citations
                
            except json.JSONDecodeError as e:
                # Fallback: create basic recommendations from text
                self.logger.warning(f"JSON parsing failed: {str(e)}")
                self.logger.info("Creating basic recommendations from text")
                basic_rec = TreatmentRecommendation(
                    category="clinical",
                    recommendation="Clinical pathway available - see evidence sources for detailed protocol",
                    priority="high",
                    duration=None,
                    notes=f"Full protocol extracted. See citations for evidence."
                )
                return [basic_rec], citations
            
            #Convert to pydantic models
            recommendations = []
            for rec_data in treatment_data.get("treatment_recommendations", []):
                recommendation = TreatmentRecommendation(
                    category=rec_data.get("category", ""),
                    recommendation=rec_data.get("recommendation", ""),
                    priority=rec_data.get("priority", "medium"),
                    duration=rec_data.get("duration"),
                    notes=rec_data.get("notes")
                )
                recommendations.append(recommendation)
            
            self.logger.info(f"Generated {len(recommendations)} treatment recommendations")
            return recommendations, citations
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error in Perplexity treatment request: {str(e)}")
            raise ValueError(f"Error communicating with Perplexity API: {str(e)}")
        
        except Exception as e:
            self.logger.error(f"Error getting treatment recommendations: {str(e)}")
            raise ValueError(f"Error in treatment recommendation: {str(e)}")
    
    def _create_treatment_prompt(self, diagnosis: Diagnosis, patient_age: int, patient_gender: str) -> str:
        """Create prompt for evidence-based clinical pathway in JSON format"""
        
        gender_text = f", {patient_gender}" if patient_gender else ""
        
        return f"""
Act as a clinical research assistant and develop a comprehensive care pathway for primary diagnosis: {diagnosis.diagnosis_name.upper()} (ICD-10: {diagnosis.icd_10_code.code}).

Patient profile: {patient_age} years old{gender_text}

Based on recent research and current clinical practice guidelines from US, Canada, and Europe (prioritize ≥2023-2025 sources: AHA/ACC, NICE, ESC, USPSTF, CDC, CADTH).

Return ONLY this JSON structure:

{{
    "clinical_pathway": [
        {{
            "recommendation": "Specific clinical recommendation with dosage/details",
            "priority": "high/medium/low",
            "duration": "timeframe or null",
            "notes": "evidence source and additional context"
        }}
    ]
}}

Include: initial assessment, treatment approach, monitoring requirements, key contraindications, and follow-up. Keep concise for demonstration. Cite guidelines in notes field.

JSON only - no additional text:
"""
    
    def _extract_json_from_response(self, content: str) -> str:
        """Extract JSON from response, handling markdown wrappers and extra text"""
        
        #Remove any markdown code blocks
        content = content.strip()
        
        # 1 - Look for JSON wrapped in markdown
        if "```json" in content:
            #Extract content between ```json and ```
            start = content.find("```json") + 7
            end = content.find("```", start)
            if end != -1:
                json_content = content[start:end].strip()
                self.logger.info("Extracted JSON from markdown wrapper")
                return json_content
        
        # 2 - Look for JSON between ``` without json specifier
        if content.startswith("```") and content.endswith("```"):
            json_content = content[3:-3].strip()
            self.logger.info("Extracted JSON from generic markdown wrapper")
            return json_content
        
        # 3 - Look for JSON object in the text (find first { and last })
        start_brace = content.find("{")
        end_brace = content.rfind("}")
        
        if start_brace != -1 and end_brace != -1 and end_brace > start_brace:
            json_content = content[start_brace:end_brace + 1]
            self.logger.info("Extracted JSON from text using brace detection")
            return json_content
        
        # If no JSON structure found, return original content
        self.logger.warning("No JSON structure detected, returning original content")
        return content
    
    def is_ready(self) -> bool:
        """Check if perplexity is ready"""
        return bool(self.api_key)