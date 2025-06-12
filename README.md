# Restful‑Booker Automation Project

This PyCharm‑ready project contains fully‑automated **API tests** (via `pytest` + `requests`) and **smoke‑level UI tests** (via `selenium`).

## Quick Start

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # adjust if you want to override credentials
pytest -v --html=report.html
```

* Selenium tests run headless Chrome by default.  
* API base‑URL & credentials can be overridden via environment variables:
  * `BASE_URL` (default `https://restful-booker.herokuapp.com`)
  * `API_USERNAME` (default `admin`)
  * `API_PASSWORD` (default `password123`)
