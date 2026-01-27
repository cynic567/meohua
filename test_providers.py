"""
Unit tests for LLM providers

运行测试 / Run tests:
    python -m pytest test_providers.py
    或 / or
    python test_providers.py
"""
import unittest
from unittest.mock import Mock, patch
from llm_provider import LLMProvider
from openai_provider import OpenAIProvider
from anthropic_provider import AnthropicProvider
from custom_provider import CustomProvider


class TestLLMProvider(unittest.TestCase):
    """Test LLM provider base class"""
    
    def test_provider_is_abstract(self):
        """Test that LLMProvider cannot be instantiated directly"""
        with self.assertRaises(TypeError):
            LLMProvider('test_key')


class TestOpenAIProvider(unittest.TestCase):
    """Test OpenAI provider"""
    
    def setUp(self):
        self.provider = OpenAIProvider('test_api_key')
    
    def test_initialization(self):
        """Test provider initialization"""
        self.assertEqual(self.provider.api_key, 'test_api_key')
        self.assertEqual(self.provider.base_url, 'https://api.openai.com/v1')
        self.assertEqual(self.provider.default_model, 'gpt-3.5-turbo')
    
    def test_custom_base_url(self):
        """Test custom base URL"""
        provider = OpenAIProvider('test_key', base_url='https://custom.api.com')
        self.assertEqual(provider.base_url, 'https://custom.api.com')
    
    def test_get_models(self):
        """Test getting available models"""
        models = self.provider.get_models()
        self.assertIsInstance(models, list)
        self.assertIn('gpt-4', models)
        self.assertIn('gpt-3.5-turbo', models)
    
    @patch('openai_provider.requests.post')
    def test_chat_success(self, mock_post):
        """Test successful chat request"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'Test response'}}]
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        messages = [{'role': 'user', 'content': 'Hello'}]
        response = self.provider.chat(messages)
        
        self.assertEqual(response, 'Test response')
        mock_post.assert_called_once()
    
    @patch('openai_provider.requests.post')
    def test_chat_error(self, mock_post):
        """Test chat request with error"""
        import requests
        mock_post.side_effect = requests.exceptions.RequestException('API Error')
        
        messages = [{'role': 'user', 'content': 'Hello'}]
        response = self.provider.chat(messages)
        
        self.assertIn('Error', response)


class TestAnthropicProvider(unittest.TestCase):
    """Test Anthropic provider"""
    
    def setUp(self):
        self.provider = AnthropicProvider('test_api_key')
    
    def test_initialization(self):
        """Test provider initialization"""
        self.assertEqual(self.provider.api_key, 'test_api_key')
        self.assertEqual(self.provider.base_url, 'https://api.anthropic.com/v1')
    
    def test_get_models(self):
        """Test getting available models"""
        models = self.provider.get_models()
        self.assertIsInstance(models, list)
        self.assertIn('claude-3-opus-20240229', models)
        self.assertIn('claude-3-sonnet-20240229', models)
    
    @patch('anthropic_provider.requests.post')
    def test_chat_success(self, mock_post):
        """Test successful chat request"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'content': [{'text': 'Test response'}]
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        messages = [{'role': 'user', 'content': 'Hello'}]
        response = self.provider.chat(messages)
        
        self.assertEqual(response, 'Test response')


class TestCustomProvider(unittest.TestCase):
    """Test Custom provider"""
    
    def setUp(self):
        self.provider = CustomProvider(
            'test_api_key',
            'https://custom.api.com',
            'custom-model'
        )
    
    def test_initialization(self):
        """Test provider initialization"""
        self.assertEqual(self.provider.api_key, 'test_api_key')
        self.assertEqual(self.provider.base_url, 'https://custom.api.com')
        self.assertEqual(self.provider.default_model, 'custom-model')
    
    def test_get_models(self):
        """Test getting available models"""
        models = self.provider.get_models()
        self.assertEqual(models, ['custom-model'])


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
