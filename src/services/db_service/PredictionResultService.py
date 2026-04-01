from models import PredictionResultModel
from uuid import UUID

class PredictionResultService:
    def __init__(self,db_client,session_id:UUID):
        self.models=PredictionResultModel(db_client=db_client,session_id=session_id)
    
    async def insert_machine_model_predict(self,prediction_value:str,confidence_score:float):
        result=await self.models.insert_machine_prediction_values(prediction_value=prediction_value,confidence_score=confidence_score)
        return result
    async def insert_deep_model_predict(self,prediction_value:str,confidence_score:float,model_name:str,model_version:str,image_id:UUID):
        result=await self.models.insert_deep_prediction_values(prediction_value=prediction_value,confidence_score=confidence_score,
                                                               model_name=model_name,model_version=model_version,image_id=image_id)
        return result