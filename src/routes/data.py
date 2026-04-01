from fastapi import APIRouter,status,Request,UploadFile, File
from fastapi.responses import JSONResponse
from controllers import ImageValidation,FeatureValidation
from services import DeepEyeClassifier,MachineEyeClassifier
from models import ResponseSignal,DataBaseResponseEnums
from .schemas import EyeFeatureSchema
from typing import List
from uuid import UUID
data_router=APIRouter(prefix="/api/data",tags=["data"])

@data_router.post("/upload/eyeImage/{session_id}")
async def upload_eye_image(images:List[UploadFile]=File(...),request:Request=None,session_id:UUID=None):

   results=[]
   for image in images:
      content=await image.read()
  
      image_validator=ImageValidation(image=image,content=content)
      valid,signal=await image_validator.all_validations()
      if not valid:
        return JSONResponse(content={"Signal":signal},status_code=status.HTTP_400_BAD_REQUEST)

      classifier=DeepEyeClassifier(content=content,db_client=request.app.db_client,session_id=session_id)
      preprocessed_image,image_id=await classifier.preprocess()
      if preprocessed_image is None:
        return JSONResponse(content={"signal":ResponseSignal.IMAGE_PREPROCESS_ERROR.value},status_code=status.HTTP_400_BAD_REQUEST)
     
      prediction_result,image_result=await classifier.predict(data=preprocessed_image,request=request,image_id=image_id)

      if prediction_result is None:
        return JSONResponse(content={"Signal":ResponseSignal.IMAGE_PREDICT_ERROR.value},status_code=status.HTTP_400_BAD_REQUEST)
      results.append({
            "filename": image.filename,
            "user_predict":prediction_result,
            "user_image":image_result
        })
   return JSONResponse(
        content={
            "signal": ResponseSignal.IMAGE_PREDICT_SUCCESSFULLY.value,
            "session_id":str(session_id),
            "results": results
        },
        status_code=status.HTTP_200_OK
    )

@data_router.post("/upload/eyefeature/{session_id}")
async def upload_eye_feature(feature:EyeFeatureSchema,request:Request,session_id:UUID):
  eye_feature_validator=FeatureValidation()
  valid,signal=await eye_feature_validator.feature_validation(feature=feature)
  if not valid:
   return JSONResponse(content={"signal":signal},status_code=status.HTTP_400_BAD_REQUEST)
  
  classifier=MachineEyeClassifier(feature=feature,db_client=request.app.db_client,session_id=session_id)
  preprocessed_data,feature_result=await classifier.preprocess()
  if not feature_result:
    return JSONResponse(content={"signal":DataBaseResponseEnums.USER_DID_NOT_HAVE_INFO.value})

  predict_result=await classifier.predict(preprocessed_feature=preprocessed_data,request=request)
  
  return JSONResponse(content={"signal":ResponseSignal.FEATURE_PREDICT_SUCCESSFULLY.value,"session_id":str(session_id),"user_feature":feature_result,"user_prediction":predict_result},status_code=status.HTTP_200_OK)
  