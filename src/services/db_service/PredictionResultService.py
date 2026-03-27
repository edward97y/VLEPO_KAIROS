from models import PredictionResultModel
from uuid import UUID

class PredictionResultService:
    def __init__(self,db_client,session_id:UUID,image_id:UUID=None):
        self.models=PredictionResultModel(db_client=db_client,session_id=session_id)
    
    async def insert_machine_model_predict(self,prediction_value:str,confidence_score:float):
        result=await self.models.insert_machine_prediction_values(prediction_value=prediction_value,confidence_score=confidence_score)
        return result