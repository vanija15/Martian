# providers/base_provider.py
from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    def set_api_key(self, api_key):
        pass

    @abstractmethod
    def create_completion(self, **kwargs):
        pass

# providers/openai_provider.py
import openai

class OpenAIProvider(BaseProvider):
    def set_api_key(self, api_key):
        openai.api_key = api_key

    def create_completion(self, **kwargs):
        return openai.Completion.create(**kwargs)

# providers/anthropic_provider.py
import anthropic

class AnthropicProvider(BaseProvider):
    def set_api_key(self, api_key):
        anthropic.api_key = api_key

    def create_completion(self, **kwargs):
        return anthropic.completion(**kwargs)

# providers/together_provider.py
import togethercall

class TogetherProvider(BaseProvider):
    def set_api_key(self, api_key):
        togethercall.api_key = api_key

    def create_completion(self, **kwargs):
        return togethercall.create_completion(**kwargs)

# models/request_models.py
from pydantic import BaseModel

class CompletionRequest(BaseModel):
    prompt: str
    max_tokens: int = 50
    temperature: float = 0.7
    top_p: float = 1.0
    stream: bool = False
    # Add other parameters as needed

# models/response_models.py
from pydantic import BaseModel

class CompletionResponse(BaseModel):
    choices: list
    # Add other fields as needed

# utils/api_utils.py
import requests

def make_request(url, headers, data):
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

# utils/exceptions.py
class InvalidAPIKeyError(Exception):
    pass

class RateLimitError(Exception):
    pass

class ProviderSpecificError(Exception):
    pass

# routes/openai_routes.py
from fastapi import APIRouter, Depends
from providers.openai_provider import OpenAIProvider
from models.request_models import CompletionRequest
from models.response_models import CompletionResponse
from utils.exceptions import InvalidAPIKeyError

router = APIRouter()

def get_provider(api_key: str):
    provider = OpenAIProvider()
    try:
        provider.set_api_key(api_key)
    except Exception as e:
        raise InvalidAPIKeyError(str(e))
    return provider

@router.post("/openai/completion", response_model=CompletionResponse)
def create_completion(request: CompletionRequest, provider: OpenAIProvider = Depends(get_provider)):
    try:
        response = provider.create_completion(**request.dict())
        return CompletionResponse.parse_obj(response)
    except Exception as e:
        raise ProviderSpecificError(str(e))

# routes/anthropic_routes.py
# ... (similar to openai_routes.py)

# routes/together_routes.py
# ... (similar to openai_routes.py)

# main.py
from fastapi import FastAPI
from routes.openai_routes import router as openai_router
from routes.anthropic_routes import router as anthropic_router
from routes.together_routes import router as together_router

app = FastAPI()
app.include_router(openai_router)
app.include_router(anthropic_router)
app.include_router(together_router)

# tests/test_providers.py
import pytest
from unittest.mock import patch
from providers.openai_provider import OpenAIProvider
from providers.anthropic_provider import AnthropicProvider
from providers.together_provider import TogetherProvider
from utils.exceptions import InvalidAPIKeyError

# Unit tests for provider classes

# tests/test_routes.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_openai_completion():
    # Integration test for OpenAI completion route
    payload = {
        "prompt": "What is the capital of France?",
        "max_tokens": 50,
        "temperature": 0.7,
        "top_p": 1.0,
        "stream": False
    }
    headers = {"Authorization": "Bearer your_api_key_here"}
    response = client.post("/openai/completion", json=payload, headers=headers)
    assert response.status_code == 200
    # Add more assertions as needed

def test_anthropic_completion():
    # Integration test for Anthropic completion route
    pass

def test_together_completion():
    # Integration test for Together completion route
    pass