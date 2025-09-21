from abc import ABC, abstractmethod
from typing import Any, Optional
import streamlit as st

class UIComponentInterface(ABC):
    """Interface para componentes UI (SRP)"""
    
    @abstractmethod
    def render(self) -> Any:
        """Render the UI component and return its value"""
        pass
    
    @abstractmethod
    def validate_input(self, value: Any) -> bool:
        """Validate component input"""
        pass