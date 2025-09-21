import streamlit as st
from typing import Dict, Any, List
from interfaces.result_formatter import ResultFormatterInterface

class MedicalResultFormatter(ResultFormatterInterface):
    """Implementación concreta para formatear resultados médicos (SRP)"""
    
    def format_transcription(self, data: Dict[str, Any]) -> None:
        """Format transcription results"""
        result = data.get('result', {})
        metadata = data.get('metadata', {})
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader("📝 Transcribed Text")
            transcription = result.get('transcription', 'No transcription available')
            st.write(transcription)
        
        with col2:
            st.subheader("📈 Metadata")
            self._render_metrics(metadata)
    
    def format_medical_extraction(self, data: Dict[str, Any]) -> None:
        """Format medical extraction results"""
        result = data.get('result', {})
        metadata = data.get('metadata', {})
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self._render_patient_info(result.get('patient_info', {}))
            self._render_symptoms(result.get('symptoms', []))
            self._render_consultation_reason(result.get('consultation_reason', ''))
        
        with col2:
            st.subheader("📊 Extraction Metadata")
            self._render_detailed_metadata(metadata)
    
    def format_diagnosis(self, data: Dict[str, Any]) -> None:
        """Format diagnosis results"""
        result = data.get('result', {})
        metadata = data.get('metadata', {})
        
        # Primary diagnosis
        if 'primary_diagnosis' in result:
            self._render_primary_diagnosis(result['primary_diagnosis'])
        
        # Differential diagnoses
        if 'differential_diagnoses' in result:
            self._render_differential_diagnoses(result['differential_diagnoses'])
        
        # Treatment plan
        if 'treatment_plan' in result:
            self._render_treatment_plan(result['treatment_plan'])
        
        # Evidence citations
        if 'evidence_citations' in result:
            self._render_evidence_citations(result['evidence_citations'])
        
        # Metadata
        self.format_metadata(metadata)
    
    def format_metadata(self, data: Dict[str, Any]) -> None:
        """Format metadata section"""
        st.subheader("📊 Processing Metadata")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'processing_time_seconds' in data:
                st.metric("Processing Time", f"{data['processing_time_seconds']:.1f}s")
        
        with col2:
            if 'primary_diagnosis_confidence' in data:
                st.metric("Primary Confidence", f"{data['primary_diagnosis_confidence']:.1%}")
        
        with col3:
            if 'diagnoses_generated' in data:
                st.metric("Diagnoses Generated", data['diagnoses_generated'])
        
        with col4:
            if 'treatment_recommendations' in data:
                st.metric("Treatment Items", data['treatment_recommendations'])
    
    def _render_patient_info(self, patient_info: Dict[str, Any]) -> None:
        """Render patient information section"""
        if not patient_info:
            return
        
        st.subheader("👤 Patient Information")
        
        info_col1, info_col2, info_col3 = st.columns(3)
        with info_col1:
            st.write(f"**Name:** {patient_info.get('name', 'N/A')}")
        with info_col2:
            st.write(f"**Age:** {patient_info.get('age', 'N/A')}")
        with info_col3:
            st.write(f"**ID:** {patient_info.get('patient_id', 'N/A')}")
    
    def _render_symptoms(self, symptoms: List[str]) -> None:
        """Render symptoms section"""
        if not symptoms:
            return
        
        st.subheader("🩺 Symptoms")
        if isinstance(symptoms, list):
            for i, symptom in enumerate(symptoms, 1):
                st.write(f"{i}. {symptom}")
        else:
            st.write(symptoms)
    
    def _render_consultation_reason(self, reason: str) -> None:
        """Render consultation reason"""
        if not reason:
            return
        
        st.subheader("📋 Consultation Reason")
        st.write(reason)
    
    def _render_primary_diagnosis(self, primary: Dict[str, Any]) -> None:
        """Render primary diagnosis with confidence styling"""
        confidence = primary.get('confidence_score', 0)
        confidence_class = self._get_confidence_class(confidence)
        
        st.markdown(f"""
        <div class="{confidence_class}">
            <h3>🎯 Primary Diagnosis</h3>
            <h4>{primary.get('diagnosis_name', 'Unknown')}</h4>
            <p><strong>Confidence:</strong> {confidence:.1%}</p>
            <p><strong>ICD-10:</strong> {primary.get('icd_10_code', {}).get('code', 'N/A')} - {primary.get('icd_10_code', {}).get('description', 'N/A')}</p>
            <p><strong>Reasoning:</strong> {primary.get('reasoning', 'No reasoning provided')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_differential_diagnoses(self, diff_diagnoses: List[Dict[str, Any]]) -> None:
        """Render differential diagnoses"""
        st.subheader("🔍 Differential Diagnoses")
        
        for i, diff_diag in enumerate(diff_diagnoses, 1):
            confidence = diff_diag.get('confidence_score', 0)
            confidence_class = self._get_confidence_class(confidence, is_differential=True)
            
            st.markdown(f"""
            <div class="{confidence_class}">
                <h5>{i}. {diff_diag.get('diagnosis_name', 'Unknown')}</h5>
                <p><strong>Confidence:</strong> {confidence:.1%}</p>
                <p><strong>ICD-10:</strong> {diff_diag.get('icd_10_code', {}).get('code', 'N/A')}</p>
                <p>{diff_diag.get('reasoning', 'No reasoning provided')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    def _render_treatment_plan(self, treatment_plan: List[Dict[str, Any]]) -> None:
        """Render treatment plan grouped by priority"""
        st.subheader("💊 Treatment Plan")
        
        # Group by priority
        high_priority = [t for t in treatment_plan if t.get('priority') == 'high']
        medium_priority = [t for t in treatment_plan if t.get('priority') == 'medium']
        low_priority = [t for t in treatment_plan if t.get('priority') == 'low']
        
        self._render_priority_treatments("🔴 High Priority", high_priority, "🚨")
        self._render_priority_treatments("🟡 Medium Priority", medium_priority, "⚠️")
        self._render_priority_treatments("🟢 Low Priority", low_priority, "ℹ️")
    
    def _render_priority_treatments(self, title: str, treatments: List[Dict[str, Any]], icon: str) -> None:
        """Render treatments for a specific priority level"""
        if not treatments:
            return
        
        st.markdown(f"**{title}:**")
        for treatment in treatments:
            recommendation = treatment.get('recommendation', 'No recommendation')
            with st.expander(f"{icon} {recommendation[:60]}..."):
                st.write(f"**Full Recommendation:** {recommendation}")
                st.write(f"**Duration:** {treatment.get('duration', 'N/A')}")
                st.write(f"**Category:** {treatment.get('category', 'N/A')}")
                if treatment.get('notes'):
                    st.write(f"**Notes:** {treatment['notes']}")
    
    def _render_evidence_citations(self, citations: List[str]) -> None:
        """Render evidence citations"""
        st.subheader("📚 Evidence Citations")
        for i, citation in enumerate(citations, 1):
            st.write(f"{i}. [{citation}]({citation})")
    
    def _render_metrics(self, metadata: Dict[str, Any]) -> None:
        """Render simple metrics"""
        if 'processing_time_seconds' in metadata:
            st.metric("Processing Time", f"{metadata['processing_time_seconds']:.2f}s")
        if 'confidence_score' in metadata:
            st.metric("Confidence", f"{metadata['confidence_score']:.2%}")
    
    def _render_detailed_metadata(self, metadata: Dict[str, Any]) -> None:
        """Render detailed metadata"""
        for key, value in metadata.items():
            if key == 'processing_time_seconds':
                st.metric("Processing Time", f"{value:.2f}s")
            elif key == 'confidence_score':
                st.metric("Confidence", f"{value:.2%}")
            else:
                st.write(f"**{key.replace('_', ' ').title()}:** {value}")
    
    def _get_confidence_class(self, confidence: float, is_differential: bool = False) -> str:
        """Get CSS class based on confidence level (OCP)"""
        if is_differential:
            if confidence >= 0.7:
                return "confidence-medium"
            else:
                return "confidence-low"
        else:
            if confidence >= 0.8:
                return "confidence-high"
            elif confidence >= 0.6:
                return "confidence-medium"
            else:
                return "confidence-low"
