from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    VERSION: str = '0.10'
    MODEL_PATH: str = 'src/ml/artifacts/model.pkl'
    MODEL_VERSION: str = 'v1-2026-08'
    CORS_ORIGIN: list[str] = ['*']
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file= '.env')

settings = Config()

        

