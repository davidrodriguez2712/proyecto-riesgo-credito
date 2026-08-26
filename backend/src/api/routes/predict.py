from fastapi import APIRouter, Depends, HTTPException
from src.models.schemas import ClienteInput, PredictionOutput
from src.services.model_services import ModelService, get_model_service
from src.config.config import settings
import logging

logger = logging.getLogger('mlops')

router = APIRouter()

def clasificar_cliente(pd):
    if pd <= 0.0121:
        return 'Bajo Riesgo'
    elif pd <= 0.031:
        return 'Medio Riesgo'
    elif pd <= 0.167:
        return 'Alto Riesgo'
    else:
        return 'Muy Alto Riesgo'

@router.post('/predict', response_model= PredictionOutput)
def predict(cliente: ClienteInput, service: ModelService = Depends(get_model_service)):

    try:
        pd = service.predict(
            features= cliente.model_dump(by_alias= True)
        )
    except Exception:
        logger.exception('Error durante la predicción')

        raise HTTPException(
            status_code= 500,
            detail= 'Error interno durante la predicción'
        )

    clasificacion_riesgo = clasificar_cliente(pd= pd)

    return PredictionOutput(
        pd_estimada= pd,
        banda_riesgo= clasificacion_riesgo,
        version_modelo= service.version
    )



