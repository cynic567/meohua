"""
OpenAI API Provider
"""
import json
import requests
from typing import Dict, List
from llm_provider import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI API provider"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1", **kwargs):
        super().__init__(api_key, **kwargs)
        self.base_url = base_url
        self.default_model = kwargs.get('model', 'gpt-3.5-turbo')
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Send chat request to OpenAI API"""
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
        """Get list of OpenAI models"""
        return [
            'gpt-4',
            'gpt-4-turbo-preview',
            'gpt-3.5-turbo',
            'gpt-3.5-turbo-16k'
        ]
