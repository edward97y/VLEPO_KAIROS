from .Modelinterface import Model_interface
from routes.schemas import EyeFeatureSchema
from helpers.config import get_settings
from fastapi import Request
import pandas as pd
import numpy as np
import uuid
from .db_service import UserFeatureService,PredictionResultService
from core.logging import get_logger

logger=get_logger(__name__)
class MachineEyeClassifier(Model_interface):
    def __init__(self,db_client,feature:EyeFeatureSchema,session_id:uuid):
        self.feature=feature
        self.settings=get_settings()
        self.session_id=session_id
        self.user_feature_db_model=UserFeatureService(session_id=session_id,db_client=db_client)
        self.prediction_result_db_model=PredictionResultService(db_client=db_client,session_id=session_id)
    
    async def calculate_bmi(self):
        logger.info(f"calculate BMI started | session_id={self.session_id}")    
        height=self.feature.height/100 #convert from cm to m
        weight=self.feature.weight
        bmi=height/(weight**2)
        logger.info(f"calculate BMI done | session_id={self.session_id} | bmi={bmi}")
        return bmi
        
    async def is_obese(self,bmi):
        result=1 if bmi > self.settings.OBESITY_BMI_THRESHOLD else 0
        logger.info(
            f"obesity check completed | session_id={self.session_id} | bmi={bmi} | obese={result}"
        )
        return result
    async def preprocess(self):
        
        logger.info(f"preprocess started | session_id={self.session_id}")
        bmi=await self.calculate_bmi()
        obesity=await self.is_obese(bmi=bmi)
        feature_dict={'age':self.feature.age, 'dm_time':self.feature.dm_time,
                    'insulin':self.feature.insulin, 'oraltreatment_dm':self.feature.oraltreatment_dm,
                    'systemic_hypertension':self.feature.systemic_hypertension, 'alcohol_consumption':self.feature.alcohol_consumption,
                    'smoking':self.feature.smoking, 'obesity':obesity,'vascular_disease':self.feature.vascular_disease,
                    'acute_myocardial_infarction':self.feature.acute_myocardial_infarction, 'nephropathy':self.feature.nephropathy,
                    'neuropathy':self.feature.neuropathy, 'diabetic_foot':self.feature.diabetic_foot}
        logger.info(
            f"feature dictionary built | session_id={self.session_id}"
        )
        
        result=await self.user_feature_db_model.insert_user_info(user_feature=feature_dict)
        logger.info(
            f"user feature stored | session_id={self.session_id} | feature_id={result.Feature_id}"
        )
        feature_result={"feature_id":str(result.Feature_id),"user_feature":result.User_Feature,"feature_session_id":str(result.Feature_Session_id)}
        feature_dataframe=pd.DataFrame([feature_dict])
        logger.info(f"preprocess completed | session_id={self.session_id}")
        return feature_dataframe,feature_result
    async def predict(self,preprocessed_feature, request:Request):
       
        logger.info(f"machine prediction started | session_id={self.session_id}")
        try:
            predict_list=request.app.machine_eye_classifier.predict(preprocessed_feature)
            predict_index=int(predict_list[0])
            confidence_list=request.app.machine_eye_classifier.predict_proba(preprocessed_feature)
            confidence = float(np.max(confidence_list))
            predict_classes=self.settings.EYE_DISEASES_CLASS_LIST_MACHINE_MODEL
            prediction=predict_classes[predict_index]
            logger.info(
                 f"model prediction done | session_id={self.session_id} | prediction={prediction} | confidence={confidence}"
             )

            result=await self.prediction_result_db_model.insert_machine_model_predict(prediction_value=prediction,confidence_score=confidence)
            logger.info(
                 f"prediction stored in DB | session_id={self.session_id} | prediction_id={result.Prediction_id}"
             )
            predict_result={"prediction_id":str(result.Prediction_id),
                            "model_name":result.model_name,
                            "prediction_value":result.prediction_value,
                            "model_version":result.model_version,
                            "confidence_score":result.confidence_score,
                            "created_at":str(result.created_at),
                            "prediction_session_id":str(result.Prediction_Session_id)}
            logger.info(f"machine prediction completed | session_id={self.session_id}")

            return predict_result
        except Exception:
            logger.error(
           f"machine prediction pipeline failed | session_id={self.session_id}",
           exc_info=True
       )
            raise