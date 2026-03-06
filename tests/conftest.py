import pytest
import respx
from httpx import Response
from jules.client import JulesClient

@pytest.fixture
def mock_api():
    with respx.mock(base_url="https://jules.googleapis.com/v1alpha") as respx_mock:
        yield respx_mock

@pytest.fixture
def client(mock_api):
    return JulesClient(api_key="test-key")
