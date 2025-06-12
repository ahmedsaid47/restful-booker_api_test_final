"""Lightweight client wrapper around the Restful‑Booker endpoints."""
import requests, random, json, time
from typing import Dict, Any
from .config import BASE_URL, USERNAME, PASSWORD, HEADERS


class RestfulBookerClient:
    def __init__(self):
        self.base = BASE_URL.rstrip("/")
        self.session = requests.Session()
        self.token = self._create_token()
        self.auth_headers = {**HEADERS, "Cookie": f"token={self.token}"}

    # ---------- Authentication ----------
    def _create_token(self) -> str:
        resp = self.session.post(
            f"{self.base}/auth",
            json={"username": USERNAME, "password": PASSWORD},
            headers=HEADERS,
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()["token"]

    # ---------- Booking helpers ----------
    def create_random_booking(self) -> Dict[str, Any]:
        payload = {
            "firstname": "Test",
            "lastname": f"User{random.randint(100,999)}",
            "totalprice": random.randint(50, 500),
            "depositpaid": random.choice([True, False]),
            "bookingdates": {"checkin": "2025-08-01", "checkout": "2025-08-10"},
            "additionalneeds": random.choice(["Breakfast", "Late checkout", "None"]),
        }
        resp = self.session.post(f"{self.base}/booking", json=payload, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def get_booking(self, booking_id: int):
        resp = self.session.get(f"{self.base}/booking/{booking_id}", headers=HEADERS, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def update_booking(self, booking_id: int, new_data: Dict[str, Any]):
        resp = self.session.put(
            f"{self.base}/booking/{booking_id}", json=new_data, headers=self.auth_headers, timeout=10
        )
        resp.raise_for_status()
        return resp.json()

    def partial_update(self, booking_id: int, patch: Dict[str, Any]):
        resp = self.session.patch(
            f"{self.base}/booking/{booking_id}", json=patch, headers=self.auth_headers, timeout=10
        )
        resp.raise_for_status()
        return resp.json()

    def delete_booking(self, booking_id: int) -> int:
        resp = self.session.delete(
            f"{self.base}/booking/{booking_id}", headers=self.auth_headers, timeout=10
        )
        return resp.status_code
