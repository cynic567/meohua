"""
Anthropic Claude API Provider
"""
import json
import requests
from typing import Dict, List
from llm_provider import LLMProvider


class AnthropicProvider(LLMProvider):
    """Anthropic Claude API provider"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.anthropic.com/v1", **kwargs):
        super().__init__(api_key, **kwargs)
        self.base_url = base_url
        self.default_model = kwargs.get('model', 'claude-3-sonnet-20240229')
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Send chat request to Anthropic API"""
        model = kwargs.get('model', self.default_model)
        temperature = kwargs.get('temperature', 0.7)
        max_tokens = kwargs.get('max_tokens', 2000)
        
        # Convert messages format to Anthropic format
        system_message = ""
        anthropic_messages = []
        for msg in messages:
            if msg['role'] == 'system':
                system_message = msg['content']
            else:
                anthropic_messages.append({
                    'role': msg['role'],
                    'content': msg['content']
                })
        
        headers = {
            'x-api-key': self.api_key,
            'anthropic-version': '2023-06-01',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': model,
            'messages': anthropic_messages,
            'max_tokens': max_tokens,
            'temperature': temperature
        }
        
        if system_message:
            data['system'] = system_message
        
        try:
            response = requests.post(
                f'{self.base_url}/messages',
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result['content'][0]['text']
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"
        except (KeyError, IndexError) as e:
            return f"Error parsing response: {str(e)}"
    
    def get_models(self) -> List[str]:
        """Get list of Anthropic models"""
        return [
            'claude-3-opus-20240229',
            'claude-3-sonnet-20240229',
            'claude-3-haiku-20240307',
            'claude-2.1',
            'claude-2.0'
        ]
