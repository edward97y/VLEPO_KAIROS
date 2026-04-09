from .BaseDataModel import BaseDataModel
from uuid import UUID
from ..db_schemas.eye_db_schemas import PredictionResult
from core.logging import get_logger

logger = get_logger(__name__)

class PredictionResultModel(BaseDataModel):
    def __init__(self, db_client:object,session_id:UUID):
        super().__init__(db_client)
        self.session_id=session_id
        
    async def insert_machine_prediction_values(self,prediction_value:str,confidence_score:float):

        logger.info(f"Inserting prediction  | session={self.session_id}")
        try:
            async with self.db_client() as session:
                async with session.begin():
                    new_predict=PredictionResult(Prediction_Session_id=self.session_id,
                                                 model_name=self.settings.EYE_MACHINE_MODEL_NAME,
                                                 prediction_value=prediction_value,
                                                 model_version=self.settings.EYE_MACHINE_MODEL_VERSION,
                                                 confidence_score=confidence_score
                                                 )
                    session.add(new_predict)
                    await session.flush()
                logger.info(f"Prediction stored | value={prediction_value} | confidence={confidence_score} |session_id={self.session_id}")  
                return new_predict
        except Exception:
            logger.error(f"insert machine prediction failed",exc_info=True)
            raise 
        
    async def insert_deep_prediction_values(self,prediction_value:str,confidence_score:float,model_name:str,model_version:str,image_id:UUID):
        logger.info(f"Inserting prediction  | session={self.session_id}")
        
        try:
            async with self.db_client() as session:
                async with session.begin():
                    new_predict=PredictionResult(Prediction_Session_id=self.session_id,
                                                 Prediction_Image_id=image_id,
                                                 model_name=model_name,
                                                 prediction_value=prediction_value,
                                                 model_version=model_version,
                                                 confidence_score=confidence_score,

                                                 )
                    session.add(new_predict)
                    await session.flush()
                logger.info(f"Prediction stored | value={prediction_value} | confidence={confidence_score}|session_id={self.session_id}|image_id={image_id}")  
                return new_predict
        except Exception:

            logger.error(f"insert deep prediction failed",exc_info=True)
            raise 
        