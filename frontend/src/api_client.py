import requests

from config import BACKEND_URL


def predict(payload: dict) -> dict:
    response = requests.post(f"{BACKEND_URL}/api/v1/predict", json=payload, timeout=10)
    response.raise_for_status()
    return response.json()


def check_health() -> bool:
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False
