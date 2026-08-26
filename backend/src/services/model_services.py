import base64
import io
from functools import lru_cache

import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
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

WATERFALL_MAX_DISPLAY = 7


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

        explanation = shap.Explanation(
            values=shap_values,
            base_values=base_value,
            data=x[0],
            feature_names=FEATURE_ORDER,
        )

        fig = plt.figure()
        shap.plots.waterfall(explanation, max_display=WATERFALL_MAX_DISPLAY, show=False)
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', dpi=150)
        plt.close(fig)
        buf.seek(0)

        return {
            'shap_waterfall_png_base64': base64.b64encode(buf.read()).decode('ascii'),
        }


@lru_cache
def get_model_service() -> ModelService:
    return ModelService(settings.MODEL_PATH)
