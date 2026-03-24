from fastapi import FastAPI
from routes.data import data_router
from tensorflow.keras import models 
import joblib
from helpers.config import get_settings
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker

async def lifespan(app:FastAPI):
    settings=get_settings()

    #db
    postgres_conn=f"postgresql+asyncpg://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_EYE_DATABASE}"
    app.db_engin=create_async_engine(postgres_conn)
    app.db_client=sessionmaker(bind=app.db_engin,class_=AsyncSession,expire_on_commit=False)

    #models
    app.deep_eye_classifier=models.load_model(settings.EYE_CLASSIFIER_MODEL_PATH)
    app.deep_eye_diseases=models.load_model(settings.EYE_DISEASES_MODEL_PATH)
    app.machine_eye_classifier=joblib.load(settings.EYE_MACHINE_MODEL_PATH)
    yield

    app.db_engin.dispose()





app=FastAPI(lifespan=lifespan)
app.include_router(data_router)