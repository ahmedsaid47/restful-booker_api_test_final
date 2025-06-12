import pytest, requests, time
from utils.config import BASE_URL, HEADERS

@pytest.mark.benchmark(group="booking_list")
def test_list_bookings_performance(benchmark):
    """
    Benchmark the performance of the booking list endpoint.

    This test measures how long it takes to retrieve the list of all bookings
    from the API. It uses pytest-benchmark to run the request multiple times
    and collect performance statistics.

    The test is marked with the 'booking_list' group to categorize it with
    other related performance tests.

    Performance metrics collected include:
    - Min/max/mean execution time
    - Standard deviation
    - Number of rounds

    Steps:
    1. Send a GET request to /booking
    2. Verify the status code is 200
    3. Measure and record the execution time
    """
    def _get():
        resp = requests.get(f"{BASE_URL}/booking", headers=HEADERS, timeout=10)
        assert resp.status_code == 200
    benchmark(_get)
