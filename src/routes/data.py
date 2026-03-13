from fastapi import APIRouter,Depends,status,Request,UploadFile
from fastapi.responses import JSONResponse
from helpers.config import get_settings,Settings
from controllers import ImageValidation
data_router=APIRouter(prefix="/api/data",tags=["data"])

@data_router.post("/upload/eyeImage")
async def upload_eye_image(image:UploadFile,settings:Settings=Depends(get_settings)):
  content=await image.read()
  image_validator=ImageValidation(image=image,content=content)
  valid,signal=await image_validator.all_validations()
  if not valid:
    return JSONResponse(content={"Signal":signal},status_code=status.HTTP_400_BAD_REQUEST)

  return JSONResponse(content={"Signal":signal},status_code=status.HTTP_200_OK)