from fastapi import FastAPI
import pandas as pd
import numpy as np
import joblib
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from src.config.config import settings
from src.api.routes import health, predict


app = FastAPI(
    title= 'Give me Credit Proyect',
    version = settings.VERSION,
    docs_url = '/docs'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins= settings.CORS_ORIGIN,
    allow_methods= ['*'],
    allow_headers= ['*']
)


app.include_router(health.router, tags= ['health'])
app.include_router(predict.router, prefix= '/api/v1', tags= ['predict'])




















