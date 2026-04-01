from uuid import UUID
from models import ImageModel

class ImageService:
    def __init__(self,db_client:object,session_id:UUID):
        self.model=ImageModel(db_client=db_client,session_id=session_id)

    async def insert_image_info(self,image):
        result= await self.model.insert_image(image=image)
        return result
    async def update_grad_cam(self,image_id:UUID,grad_cam_image):
        result=await self.model.update_gradcam_path(image_id=image_id,grad_cam_image=grad_cam_image)
        return result
