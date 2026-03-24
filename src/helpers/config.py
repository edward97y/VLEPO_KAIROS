from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    EYE_IMAGE_SIZE:int #MB
    EYE_IMAGE_TYPE:list[str]
    EYE_IMAGE_DIMENSION:tuple[int,int]
    
   # deep eye model
    EYE_CLASSIFIER_MODEL_PATH:str
    EYE_DISEASES_MODEL_PATH:str
    EYE_CLASS_LIST:list[str]
    EYE_DISEASES_CLASS_LIST:list[str]


    #Machine eye validation
    MIN_AGE:int
    MAX_AGE:int
    MIN_DM_TIME:int
    MAX_DM_TIME:int
    MIN_WEIGHT_KG:int
    MAX_WEIGHT_KG:int
    MIN_HEIGHT_CM:int
    MAX_HEIGHT_CM:int
    OBESITY_BMI_THRESHOLD:int 
    #Machine learning model for eye classification
    EYE_MACHINE_MODEL_PATH:str
    EYE_DISEASES_CLASS_LIST_MACHINE_MODEL:list[str]
    #Postgres database config
    POSTGRES_USERNAME:str
    POSTGRES_PASSWORD:str
    POSTGRES_HOST:str
    POSTGRES_PORT:int
    POSTGRES_EYE_DATABASE:str

    model_config = SettingsConfigDict(env_file=".env")

def get_settings():
    return Settings()