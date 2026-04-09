from models import PredictionResultModel
from uuid import UUID
from core.logging import get_logger

logger=get_logger(__name__)
class PredictionResultService:
    def __init__(self,db_client,session_id:UUID):
        self.models=PredictionResultModel(db_client=db_client,session_id=session_id)
        self.session_id=session_id
    
    async def insert_machine_model_predict(self,prediction_value:str,confidence_score:float):
        logger.info(f" insert machine prediction request | session_id={self.session_id}")
        try:
            result=await self.models.insert_machine_prediction_values(prediction_value=prediction_value,confidence_score=confidence_score)
            logger.info(f" insert machine prediction complete | session_id={self.session_id}")
            return result
        except Exception:
            logger.error(f"Machine prediction insert failed | session_id={self.session_id} | "
            f"prediction_value={prediction_value} | confidence_score={confidence_score}",
            exc_info=True)
            raise
    async def insert_deep_model_predict(self,prediction_value:str,confidence_score:float,model_name:str,model_version:str,image_id:UUID):
        logger.info(f" insert machine prediction request | session_id={self.session_id}")
        try:
            result=await self.models.insert_deep_prediction_values(prediction_value=prediction_value,confidence_score=confidence_score,
                                                                   model_name=model_name,model_version=model_version,image_id=image_id)
            logger.info(f" insert deep prediction complete | session_id={self.session_id}")
            return result
        except Exception:
            logger.error( f"Deep prediction insert failed | session_id={self.session_id} | "
            f"image_id={image_id} | model={model_name} | version={model_version} | "
            f"prediction_value={prediction_value} | confidence_score={confidence_score}",
            exc_info=True
        )
            raise