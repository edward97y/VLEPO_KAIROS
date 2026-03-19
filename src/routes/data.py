from fastapi import APIRouter,status,Request,UploadFile, File
from fastapi.responses import JSONResponse
from controllers import ImageValidation,FeatureValidation
from services import DeepEyeClassifier,MachineEyeClassifier
from models import ResponseSignal
from .schemas import EyeFeatureSchema
from typing import List
data_router=APIRouter(prefix="/api/data",tags=["data"])

@data_router.post("/upload/eyeImage")
async def upload_eye_image(images:List[UploadFile]=File(...),request:Request= None):

   results=[]
   for image in images:
      content=await image.read()
  
      image_validator=ImageValidation(image=image,content=content)
      valid,signal=await image_validator.all_validations()
      if not valid:
        return JSONResponse(content={"Signal":signal},status_code=status.HTTP_400_BAD_REQUEST)

      classifier=DeepEyeClassifier(content=content)
      preprocessed_image=await classifier.preprocess()
      if preprocessed_image is None:
        return JSONResponse(content={"signal":ResponseSignal.IMAGE_PREPROCESS_ERROR.value},status_code=status.HTTP_400_BAD_REQUEST)

      image_prediction,confidence=await classifier.predict(data=preprocessed_image,request=request)

      if image_prediction is None:
        return JSONResponse(content={"Signal":ResponseSignal.IMAGE_PREDICT_ERROR.value},status_code=status.HTTP_400_BAD_REQUEST)
      results.append({
            "filename": image.filename,
            "prediction": image_prediction,
            "confidence": confidence
        })
   return JSONResponse(
        content={
            "signal": ResponseSignal.IMAGE_PREDICT_SUCCESSFULLY.value,
            "results": results
        },
        status_code=status.HTTP_200_OK
    )

@data_router.post("/upload/eyefeature")
async def upload_eye_feature(feature:EyeFeatureSchema,request:Request):
  eye_feature_validator=FeatureValidation()
  valid,signal=await eye_feature_validator.feature_validation(feature=feature)
  if not valid:
   return JSONResponse(content={"signal":signal},status_code=status.HTTP_400_BAD_REQUEST)
  classifier=MachineEyeClassifier(feature=feature)
  preprocessed_data=await classifier.preprocess()
  predict,confidence=await classifier.predict(preprocessed_feature=preprocessed_data,request=request)
  
  return JSONResponse(content={"signal":ResponseSignal.FEATURE_PREDICT_SUCCESSFULLY.value,"prediction":predict,"confidence":confidence},status_code=status.HTTP_200_OK)
  