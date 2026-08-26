import os

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8082")

RISK_BAND_COLORS = {
    "Bajo Riesgo": "#2ecc71",
    "Medio Riesgo": "#f1c40f",
    "Alto Riesgo": "#e67e22",
    "Muy Alto Riesgo": "#e74c3c",
}
