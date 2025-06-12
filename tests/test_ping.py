import requests
from utils.config import BASE_URL

def test_healthcheck_ping():
    """
    Test the health check endpoint of the API.

    This test verifies that the API is up and running by sending a request
    to the /ping endpoint, which is a health check endpoint provided by
    the Restful Booker API.

    According to the API documentation, the /ping endpoint should return
    a 201 status code when the API is healthy and operational.

    This test is critical as it validates the basic availability of the API
    and should be run before other tests to ensure the API is accessible.

    Steps:
    1. Send a GET request to the /ping endpoint
    2. Verify that the response status code is 201, indicating the API is healthy
    """
    resp = requests.get(f"{BASE_URL}/ping", timeout=5)
    # According to docs /ping should return 201 when healthy
    assert resp.status_code == 201
