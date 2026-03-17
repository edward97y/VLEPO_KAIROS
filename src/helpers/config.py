from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    IMAGE_SIZE:int #MB
    IMAGE_TYPE:list[str]
    IMAGE_DIMENSION:tuple[int,int]
    
   # deep eye model
    EYE_CLASSIFIER_MODEL_PATH:str
    EYE_DISEASES_MODEL_PATH:str
    EYE_CLASS_LIST:list[str]
    EYE_DISEASES_CLASS_LIST:list[str]


    model_config = SettingsConfigDict(env_file=".env")

def get_settings():
    return Settings()