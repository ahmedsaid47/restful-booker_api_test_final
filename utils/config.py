"""Centralised configuration values."""
import os
BASE_URL = os.getenv("BASE_URL", "https://restful-booker.herokuapp.com")
USERNAME = os.getenv("API_USERNAME", "admin")
PASSWORD = os.getenv("API_PASSWORD", "password123")
HEADERS  = {"Content-Type": "application/json"}
