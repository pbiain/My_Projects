import os
from abc import ABC, abstractmethod
from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class LLMProvider(ABC):
    """Abstract Base Class for LLM Providers."""
    @abstractmethod
    def generate(self, prompt: str, temperature: float) -> str:
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"

    def generate(self, prompt: str, temperature: float) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.choices[0].message.content

class AnthropicProvider(LLMProvider):
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-5"

    def generate(self, prompt: str, temperature: float) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.content[0].text

class LLMFactory:
    """The 'Switch' that gives you the right provider."""
    @staticmethod
    def get_provider(name: str) -> LLMProvider:
        providers = {
            "openai": OpenAIProvider,
            "anthropic": AnthropicProvider
        }
        if name.lower() not in providers:
            raise ValueError(f"Provider {name} not supported.")
        return providers[name.lower()]()