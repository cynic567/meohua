"""
LLM Provider Base Class
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, api_key: str, **kwargs):
        self.api_key = api_key
        self.config = kwargs
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Send a chat request to the LLM
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Response text from the LLM
        """
        pass
    
    @abstractmethod
    def get_models(self) -> List[str]:
        """
        Get list of available models for this provider
        
        Returns:
            List of model names
        """
        pass
