import pytest
from unittest.mock import patch 
from fastapi.testclient import TestClient


from app.app import app

@pytest.fixture
def client():
    """FastAPI Client"""
    return TestClient(app)

@pytest.fixture
def mock_settings():
    """Mock das configurações"""
    with patch('app.app.settings') as mock:
        yield mock


def test_triage_missing_api_key(client, mock_settings):
    """Test if API_KEY is missing"""
    mock_settings.openai_api_key = None
    
    response = client.post(
        "/triage",
        json={"message": "Teste de mensagem"}
    )
    
    assert response.status_code == 503
    assert response.json() == {"detail": "Missing OpenAI API KEY"}
