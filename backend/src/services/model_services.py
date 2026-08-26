import joblib
from src.config.config import settings
from functools import lru_cache


class ModelService:
    def __init__(self, model_path: str):
        self.model_path = joblib.load(model_path)
        self.version = settings.MODEL_VERSION

    def predict(self, features: dict) -> float:
        x = [[
            features['RevolvingUtilizationOfUnsecuredLines'],
            features['age'],
            features['NumberOfTime30-59DaysPastDueNotWorse'],
            features['DebtRatio'],
            features['MonthlyIncome'],
            features['NumberOfOpenCreditLinesAndLoans'],
            features['NumberOfTimes90DaysLate'],
            features['NumberRealEstateLoansOrLines'],
            features['NumberOfTime60-89DaysPastDueNotWorse'],
            features['NumberOfDependents']
        ]]
        return float(self.model_path.predict_proba(x)[0][1])

@lru_cache
def get_model_service() -> ModelService:
    return ModelService(settings.MODEL_PATH)






