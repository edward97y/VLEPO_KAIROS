from .BaseControllers import BaseControllers
from fastapi import UploadFile
from models import ResponseSignal
from PIL import Image
import io
from core.logging import get_logger

logger=get_logger(__name__)
class ImageValidation(BaseControllers):
    def __init__(self,image:UploadFile,content):
        super().__init__()
        self.BYTES_IN_MB=1024*1024 # to convert the size of the .env from number like 4 5 byte to mb 
        self.image=image
        self.content=content
    
    async def image_type_validation(self):
        logger.debug("checking image type")
        content_type=self.image.content_type
     
        if content_type not in self.settings.EYE_IMAGE_TYPE:
            logger.info(f"invalid image type : {content_type}")
            return False
        return True
    
    async def image_size_validation(self):
        logger.debug("checking image size")
        image_size=self.image.size

        if image_size > (self.settings.EYE_IMAGE_SIZE*self.BYTES_IN_MB):
            logger.warning(f"image too large:{image_size/self.BYTES_IN_MB} mb")
            return False 
        return True
    
    async def image_dimension_validation(self):
        logger.debug("checking image dimensions")
        content=self.content
        try:
            img=Image.open(io.BytesIO(content))
        except Exception as e:
            logger.error(f"image open failed :{e}")
            return False
        width, height = img.size
        if width<self.settings.EYE_IMAGE_DIMENSION[0] or height<self.settings.EYE_IMAGE_DIMENSION[1]:
            logger.warning(f"Image too small: {width}x{height}")
            return False
        return True
    

    async def all_validations(self):
        logger.info("Image validation started")
        if not await self.image_type_validation():
            return False,ResponseSignal.IMAGE_TYPE_NOT_SUPPORTED.value
        
        if not await self.image_size_validation():
            return False,ResponseSignal.IMAGE_SIZE_EXCEEDED.value
        
        if not await self.image_dimension_validation():
            return False,ResponseSignal.IMAGE_RESOLUTION_ERROR.value
        logger.info("Image validation passed")

        return True,ResponseSignal.IMAGE_VALIDATION_SUCCESSFULLY.value
