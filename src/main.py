from fastapi import FastAPI
from routes.data import data_router

app=FastAPI()
app.include_router(data_router)