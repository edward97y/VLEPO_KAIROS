from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    IMAGE_SIZE:int #MB
    IMAGE_TYPE:list[str]
    IMAGE_DIMENSION:tuple[int,int]

    model_config = SettingsConfigDict(env_file=".env")

def get_settings():
    return Settings()