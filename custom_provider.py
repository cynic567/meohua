"""
Custom API Provider for other LLM services
"""
import json
import requests
from typing import Dict, List
from llm_provider import LLMProvider


class CustomProvider(LLMProvider):
    """Custom API provider for compatible services"""
    
    def __init__(self, api_key: str, base_url: str, model: str = "default", **kwargs):
        super().__init__(api_key, **kwargs)
        self.base_url = base_url.rstrip('/')
        self.default_model = model
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Send chat request to custom API endpoint"""
        model = kwargs.get('model', self.default_model)
        temperature = kwargs.get('temperature', 0.7)
        max_tokens = kwargs.get('max_tokens', 2000)
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': model,
            'messages': messages,
            'temperature': temperature,
            'max_tokens': max_tokens
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"
        except (KeyError, IndexError) as e:
            return f"Error parsing response: {str(e)}"
    
    def get_models(self) -> List[str]:
        """Get list of models"""
        return [self.default_model]
