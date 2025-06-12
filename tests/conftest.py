import pytest, os, requests
from utils.config import BASE_URL, USERNAME, PASSWORD, HEADERS

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL.rstrip("/")

@pytest.fixture(scope="session")
def token(base_url):
    resp = requests.post(f"{base_url}/auth", json={"username": USERNAME, "password": PASSWORD}, headers=HEADERS, timeout=10)
    assert resp.status_code == 200 and "token" in resp.json(), "Auth failed"
    return resp.json()["token"]

@pytest.fixture
def auth_headers(token):
    return {**HEADERS, "Cookie": f"token={token}"}
