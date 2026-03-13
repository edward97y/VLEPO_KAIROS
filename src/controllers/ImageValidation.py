from .BaseControllers import BaseControllers
from fastapi import UploadFile
from models import ResponseSignal
from PIL import Image
import io
class ImageValidation(BaseControllers):
    def __init__(self,image:UploadFile,content):
        super().__init__()
        self.BYTES_IN_MB=1024*1024 # to convert the size of the .env from number like 4 5 byte to mb 
        self.image=image
        self.content=content
    
    async def image_type_validation(self):

        content_type=self.image.content_type
        print(content_type)
        if content_type not in self.settings.IMAGE_TYPE:
            return False
        return True
    
    async def image_size_validation(self):

        image_size=self.image.size

        if image_size > (self.settings.IMAGE_SIZE*self.BYTES_IN_MB):
            return False 
        return True
    
    async def image_dimension_validation(self):
        content=self.content
        try:
            img=Image.open(io.BytesIO(content))
        except Exception as e:
            return f"error when open an image :{e}"
        width, height = img.size
        if width<self.settings.IMAGE_DIMENSION[0] or height<self.settings.IMAGE_DIMENSION[1]:
            return False
        return True
    

    async def all_validations(self):
        if not await self.image_type_validation():
            return False,ResponseSignal.IMAGE_TYPE_NOT_SUPPORTED.value
        
        if not await self.image_size_validation():
            return False,ResponseSignal.IMAGE_SIZE_EXCEEDED.value
        
        if not await self.image_dimension_validation():
            return False,ResponseSignal.IMAGE_RESOLUTION_ERROR.value
        
        return True,ResponseSignal.IMAGE_VALIDATION_SUCCESSFULLY.value
