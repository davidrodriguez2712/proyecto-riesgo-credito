import math
from functools import lru_cache

import joblib
import shap
from src.config.config import settings

FEATURE_ORDER = [
    'RevolvingUtilizationOfUnsecuredLines',
    'age',
    'NumberOfTime30-59DaysPastDueNotWorse',
    'DebtRatio',
    'MonthlyIncome',
    'NumberOfOpenCreditLinesAndLoans',
    'NumberOfTimes90DaysLate',
    'NumberRealEstateLoansOrLines',
    'NumberOfTime60-89DaysPastDueNotWorse',
    'NumberOfDependents',
]

TOP_N_FEATURES = 6


def _sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))


class ModelService:
    def __init__(self, model_path: str):
        self.model_path = joblib.load(model_path)
        self.version = settings.MODEL_VERSION
        self.explainer = shap.TreeExplainer(self.model_path)

    def predict(self, features: dict) -> float:
        x = [[features[nombre] for nombre in FEATURE_ORDER]]
        return float(self.model_path.predict_proba(x)[0][1])

    def explain(self, features: dict) -> dict:
        x = [[features[nombre] for nombre in FEATURE_ORDER]]

        shap_values = self.explainer.shap_values(x)[0]
        base_value = self.explainer.expected_value
        base_value = base_value if not hasattr(base_value, '__len__') else base_value[-1]

        ordenado = sorted(
            zip(FEATURE_ORDER, x[0], shap_values),
            key=lambda item: abs(item[2]),
            reverse=True,
        )
        top = ordenado[:TOP_N_FEATURES]
        resto = ordenado[TOP_N_FEATURES:]

        contribuciones = []
        running_margin = base_value
        prev_prob = _sigmoid(running_margin)

        for nombre, valor, margin_shap in top:
            running_margin += margin_shap
            new_prob = _sigmoid(running_margin)
            contribuciones.append({
                'feature': nombre,
                'valor_cliente': float(valor),
                'contribucion_pp': new_prob - prev_prob,
            })
            prev_prob = new_prob

        margin_resto = sum(item[2] for item in resto)
        running_margin += margin_resto
        new_prob = _sigmoid(running_margin)
        contribuciones.append({
            'feature': 'Otras features',
            'valor_cliente': None,
            'contribucion_pp': new_prob - prev_prob,
        })

        return {
            'base_pd': _sigmoid(base_value),
            'shap_contributions': contribuciones,
        }


@lru_cache
def get_model_service() -> ModelService:
    return ModelService(settings.MODEL_PATH)
