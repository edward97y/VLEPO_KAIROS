from fastapi import APIRouter,status,Request,UploadFile
from fastapi.responses import JSONResponse
from controllers import ImageValidation
from services import DeepEyeClassifier
from models import ResponseSignal
data_router=APIRouter(prefix="/api/data",tags=["data"])

@data_router.post("/upload/eyeImage")
async def upload_eye_image(image:UploadFile,request:Request):

  content=await image.read()
 
  image_validator=ImageValidation(image=image,content=content)
  valid,signal=await image_validator.all_validations()
  if not valid:
    return JSONResponse(content={"Signal":signal},status_code=status.HTTP_400_BAD_REQUEST)

  classifier=DeepEyeClassifier(content=content)
  preprocessed_image=classifier.preprocess()
  if preprocessed_image is None:
    return JSONResponse(content={"signal":ResponseSignal.IMAGE_PREPROCESS_ERROR.value},status_code=status.HTTP_400_BAD_REQUEST)

  image_prediction,confidence=classifier.predict(data=preprocessed_image,request=request)
  
  if image_prediction is None:
    return JSONResponse(content={"Signal":ResponseSignal.IMAGE_PREDICT_ERROR.value},status_code=status.HTTP_400_BAD_REQUEST)
  return JSONResponse(content={"signal":ResponseSignal.IMAGE_PREDICT_SUCCESSFULLY.value,"prediction":image_prediction,"confidence":confidence},status_code=status.HTTP_200_OK)

  
  