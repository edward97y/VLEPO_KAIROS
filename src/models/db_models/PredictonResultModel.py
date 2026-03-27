from .BaseDataModel import BaseDataModel
from uuid import UUID
from ..db_schemas.eye_db_schemas import PredictionResult
class PredictionResultModel(BaseDataModel):
    def __init__(self, db_client,session_id:UUID,image_id:UUID=None):
        super().__init__(db_client)
        self.session_id=session_id
        self.image_id=image_id
    async def insert_machine_prediction_values(self,prediction_value:str,confidence_score:float):
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
            return new_predict
    