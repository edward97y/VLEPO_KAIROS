from .Modelinterface import Model_interface
from routes.schemas import EyeFeatureSchema
from helpers.config import get_settings
from fastapi import Request
import pandas as pd
import numpy as np
import uuid
from .db_service import UserFeatureService,PredictionResultService
class MachineEyeClassifier(Model_interface):
    def __init__(self,db_client,feature:EyeFeatureSchema,session_id:uuid):
        self.feature=feature
        self.settings=get_settings()
        self.user_feature_db_model=UserFeatureService(session_id=session_id,db_client=db_client)
        self.prediction_result_db_model=PredictionResultService(db_client=db_client,session_id=session_id)
    
    async def calculate_bmi(self):
        height=self.feature.height/100 #convert from cm to m
        weight=self.feature.weight
        bmi=height/(weight**2)
        return bmi
        
    async def is_obese(self,bmi):
        return 1 if bmi > self.settings.OBESITY_BMI_THRESHOLD else 0
    async def preprocess(self):
        
        bmi=await self.calculate_bmi()
        obesity=await self.is_obese(bmi=bmi)
        feature_dict={'age':self.feature.age, 'dm_time':self.feature.dm_time,
                    'insulin':self.feature.insulin, 'oraltreatment_dm':self.feature.oraltreatment_dm,
                    'systemic_hypertension':self.feature.systemic_hypertension, 'alcohol_consumption':self.feature.alcohol_consumption,
                    'smoking':self.feature.smoking, 'obesity':obesity,'vascular_disease':self.feature.vascular_disease,
                    'acute_myocardial_infarction':self.feature.acute_myocardial_infarction, 'nephropathy':self.feature.nephropathy,
                    'neuropathy':self.feature.neuropathy, 'diabetic_foot':self.feature.diabetic_foot}
        
        result=await self.user_feature_db_model.insert_user_info(user_feature=feature_dict)
        feature_result={"feature_id":str(result.Feature_id),"user_feature":result.User_Feature,"feature_session_id":str(result.Feature_Session_id)}
        feature_dataframe=pd.DataFrame([feature_dict])
        return feature_dataframe,feature_result
    async def predict(self,preprocessed_feature, request:Request):

       predict_list=request.app.machine_eye_classifier.predict(preprocessed_feature)
       predict_index=int(predict_list[0])
       confidence_list=request.app.machine_eye_classifier.predict_proba(preprocessed_feature)
       confidence = float(np.max(confidence_list))
       predict_classes=self.settings.EYE_DISEASES_CLASS_LIST_MACHINE_MODEL
       prediction=predict_classes[predict_index]

       result=await self.prediction_result_db_model.insert_machine_model_predict(prediction_value=prediction,confidence_score=confidence)
       predict_result={"prediction_id":str(result.Prediction_id),
                       "model_name":result.model_name,
                       "prediction_value":result.prediction_value,
                       "model_version":result.model_version,
                       "confidence_score":result.confidence_score,
                       "updated_at":str(result.Updated_at),
                       "prediction_session_id":str(result.Prediction_Session_id)}
       return predict_result