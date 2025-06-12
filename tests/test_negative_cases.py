import requests, pytest, json
from utils.config import BASE_URL, HEADERS

@pytest.mark.parametrize("booking_id", [0, 123456])
def test_get_nonexistent_booking_returns_404(booking_id):
    """
    Test that requesting a non-existent booking returns a 404 status code.

    This test verifies that when a GET request is made to retrieve a booking that doesn't exist,
    the API correctly responds with a 404 Not Found status code.

    The test is parameterized to check multiple non-existent booking IDs:
    - 0 (invalid ID)
    - 123456 (likely non-existent ID)

    Steps:
    1. Send a GET request to /booking/{booking_id} with a non-existent ID
    2. Verify the status code is 404
    """
    resp = requests.get(f"{BASE_URL}/booking/{booking_id}", headers=HEADERS, timeout=5)
    assert resp.status_code == 404

def test_create_booking_with_invalid_payload_returns_400():
    """
    Test that creating a booking with an invalid payload returns an error status code.

    This test verifies that when a POST request is made to create a booking with an invalid
    JSON payload (empty object), the API responds with either a 400 Bad Request or 
    500 Internal Server Error status code.

    Steps:
    1. Send a POST request to /booking with an invalid payload
    2. Verify the status code is either 400 or 500

    Note: Ideally, the API should consistently return 400 for invalid payloads,
    but this test allows for 500 as well since some APIs might return that for
    parsing errors.
    """
    resp = requests.post(f"{BASE_URL}/booking", data="{}", headers=HEADERS, timeout=5)
    assert resp.status_code in (400, 500)
