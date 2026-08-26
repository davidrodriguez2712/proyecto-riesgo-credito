from pydantic import BaseModel, Field
from typing import Annotated


class ClienteInput(BaseModel):
    RevolvingUtilizationOfUnsecuredLines: float
    age: int
    NumberOfTime30_59DaysPastDueNotWorse: int = Field(
        alias= 'NumberOfTime30-59DaysPastDueNotWorse'
    )
    DebtRatio: float
    MonthlyIncome: float
    NumberOfOpenCreditLinesAndLoans: int
    NumberOfTimes90DaysLate: int
    NumberRealEstateLoansOrLines: int
    NumberOfTime60_89DaysPastDueNotWorse: int = Field(
        alias= 'NumberOfTime60-89DaysPastDueNotWorse'
    )
    NumberOfDependents: float

    model_config = {'populate_by_name': True}


class PredictionOutput(BaseModel):
    pd_estimada: float
    banda_riesgo: str
    version_modelo: str
    shap_waterfall_png_base64: str