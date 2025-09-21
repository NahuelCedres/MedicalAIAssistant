import streamlit as st

class AppStyles:
    """Clase para manejar todos los estilos CSS de la app (SRP)"""
    
    @staticmethod
    def load_custom_css() -> None:
        """Load custom CSS styles"""
        st.markdown("""
        <style>
            .main-header {
                font-size: 3rem;
                color: #1f77b4;
                text-align: center;
                margin-bottom: 2rem;
                font-weight: bold;
            }
            
            .section-header {
                font-size: 1.5rem;
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 0.5rem;
                margin: 1.5rem 0 1rem 0;
            }
            
            .confidence-high {
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
                border-radius: 0.375rem;
                padding: 1rem;
                margin: 0.5rem 0;
                border-left: 4px solid #28a745;
            }
            
            .confidence-medium {
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 0.375rem;
                padding: 1rem;
                margin: 0.5rem 0;
                border-left: 4px solid #ffc107;
            }
            
            .confidence-low {
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                border-radius: 0.375rem;
                padding: 1rem;
                margin: 0.5rem 0;
                border-left: 4px solid #dc3545;
            }
            
            .processing-step {
                background-color: #e7f3ff;
                border: 1px solid #b3d9ff;
                border-radius: 0.375rem;
                padding: 0.75rem;
                margin: 0.5rem 0;
                font-weight: 500;
            }
            
            .error-box {
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                border-radius: 0.375rem;
                padding: 1rem;
                margin: 0.5rem 0;
                color: #721c24;
            }
            
            .success-box {
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
                border-radius: 0.375rem;
                padding: 1rem;
                margin: 0.5rem 0;
                color: #155724;
            }
            
            .warning-box {
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 0.375rem;
                padding: 1rem;
                margin: 0.5rem 0;
                color: #856404;
            }
            
            .metric-card {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 0.375rem;
                padding: 1rem;
                text-align: center;
                margin: 0.25rem;
            }
            
            .priority-high {
                border-left: 4px solid #dc3545;
                background-color: #fdf2f2;
            }
            
            .priority-medium {
                border-left: 4px solid #ffc107;
                background-color: #fffcf2;
            }
            
            .priority-low {
                border-left: 4px solid #28a745;
                background-color: #f2f9f2;
            }
            
            .footer {
                text-align: center;
                color: #7f8c8d;
                font-size: 0.9rem;
                margin-top: 2rem;
                padding-top: 1rem;
                border-top: 1px solid #dee2e6;
            }
            
            .sidebar-section {
                background-color: #f8f9fa;
                border-radius: 0.375rem;
                padding: 1rem;
                margin: 0.5rem 0;
            }
            
            /* Streamlit specific overrides */
            .stTextInput > div > div > input {
                background-color: #ffffff;
            }
            
            .stTextArea > div > div > textarea {
                background-color: #ffffff;
            }
            
            .stSelectbox > div > div > select {
                background-color: #ffffff;
            }
            
            /* Tab styling */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
            }
            
            .stTabs [data-baseweb="tab"] {
                height: 50px;
                padding-left: 20px;
                padding-right: 20px;
                background-color: #f0f2f6;
                border-radius: 5px 5px 0px 0px;
                font-weight: 500;
            }
            
            .stTabs [aria-selected="true"] {
                background-color: #ffffff;
                border-bottom: 2px solid #3498db;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_header(title: str) -> None:
        """Render main header"""
        st.markdown(f'<h1 class="main-header">{title}</h1>', unsafe_allow_html=True)
    
    @staticmethod
    def render_section_header(title: str) -> None:
        """Render section header"""
        st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)
    
    @staticmethod
    def render_footer() -> None:
        """Render footer"""
        st.markdown("---")
        st.markdown(
            """
            <div class="footer">
                Medical AI Assistant - Technical Demo<br>
                ⚠️ For demonstration purposes only. Not for actual medical use.
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    @staticmethod
    def render_processing_step(message: str) -> None:
        """Render processing step indicator"""
        st.markdown(f'<div class="processing-step">🔄 {message}</div>', unsafe_allow_html=True)
    
    @staticmethod
    def render_success_message(message: str) -> None:
        """Render success message"""
        st.markdown(f'<div class="success-box">✅ {message}</div>', unsafe_allow_html=True)
    
    @staticmethod
    def render_error_message(message: str) -> None:
        """Render error message"""
        st.markdown(f'<div class="error-box">❌ {message}</div>', unsafe_allow_html=True)
    
    @staticmethod
    def render_warning_message(message: str) -> None:
        """Render warning message"""
        st.markdown(f'<div class="warning-box">⚠️ {message}</div>', unsafe_allow_html=True)