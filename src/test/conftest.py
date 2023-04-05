import os
import pytest

@pytest.fixture(scope="session")
def spatineo_api_access_key():
    return os.environ.get("SPATINEO_API_ACCESS_KEY")
