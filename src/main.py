from fastapi import FastAPI
from routes.data import data_router
from tensorflow.keras import models 
import joblib
from helpers.config import get_settings
async def lifespan(app:FastAPI):
    settings=get_settings()
    app.deep_eye_classifier=models.load_model(settings.EYE_CLASSIFIER_MODEL_PATH)
    app.deep_eye_diseases=models.load_model(settings.EYE_DISEASES_MODEL_PATH)
    app.machine_eye_classifier=joblib.load(settings.EYE_MACHINE_MODEL_PATH)
    yield

    print("Shutting down...")





app=FastAPI(lifespan=lifespan)
app.include_router(data_router)