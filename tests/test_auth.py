import requests, pytest
from utils.config import BASE_URL, USERNAME, PASSWORD, HEADERS

def test_valid_auth_returns_token():
    """
    Test that valid authentication credentials return a token.

    This test verifies that when valid username and password are provided to the /auth endpoint,
    the API responds with a 200 status code and a token in the response body.

    Steps:
    1. Send a POST request to /auth with valid credentials
    2. Verify the status code is 200
    3. Verify the response contains a token
    """
    resp = requests.post(f"{BASE_URL}/auth", json={"username": USERNAME, "password": PASSWORD}, headers=HEADERS, timeout=10)
    assert resp.status_code == 200
    assert "token" in resp.json() and resp.json()["token"], "Missing token in response"

@pytest.mark.parametrize("username,password", [("bad","bad"), ("admin","bad"), ("","")])
def test_invalid_auth(username, password):
    """
    Test that invalid authentication credentials return an error message.

    This test verifies that when invalid credentials are provided to the /auth endpoint,
    the API responds with a 200 status code and a "Bad credentials" message.

    The test is parameterized to check multiple invalid credential combinations:
    - Invalid username and password
    - Valid username but invalid password
    - Empty username and password

    Steps:
    1. Send a POST request to /auth with invalid credentials
    2. Verify the status code is 200
    3. Verify the response contains the "Bad credentials" message
    """
    resp = requests.post(f"{BASE_URL}/auth", json={"username": username, "password": password}, headers=HEADERS, timeout=10)
    assert resp.status_code == 200
    assert resp.json().get("reason") == "Bad credentials"
