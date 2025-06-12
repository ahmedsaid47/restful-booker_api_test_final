from utils.api_client import RestfulBookerClient
import pytest

client = RestfulBookerClient()

def test_create_get_update_delete_booking():
    """
    Test the complete CRUD (Create, Read, Update, Delete) cycle for a booking.

    This test verifies that all booking operations work correctly in sequence:
    - Creating a new booking
    - Retrieving the booking details
    - Updating the booking with new information
    - Partially updating specific fields
    - Deleting the booking
    - Confirming the booking no longer exists

    This is an end-to-end test that validates the entire booking lifecycle
    and ensures that all API endpoints for booking management work correctly.

    Steps:
    1. Create a new booking and verify it has an ID
    2. Retrieve the booking details and verify the data is correct
    3. Update the booking with new information and verify the changes
    4. Partially update specific fields and verify the changes
    5. Delete the booking and verify the operation was successful
    6. Confirm the booking no longer exists by checking for a 404 response
    """
    # Create
    booking = client.create_random_booking()
    booking_id = booking["bookingid"]
    assert booking_id

    # Read
    details = client.get_booking(booking_id)
    assert details["firstname"] == "Test"

    # Update
    updated = client.update_booking(booking_id, {**details, "firstname": "Updated"})
    assert updated["firstname"] == "Updated"

    # Partial update
    patched = client.partial_update(booking_id, {"lastname": "Patched"})
    assert patched["lastname"] == "Patched"

    # Delete
    status = client.delete_booking(booking_id)
    assert status == 201

    # Confirm deletion
    import requests, time
    from utils.config import BASE_URL
    time.sleep(1)
    resp = requests.get(f"{BASE_URL}/booking/{booking_id}", timeout=5)
    assert resp.status_code == 404
