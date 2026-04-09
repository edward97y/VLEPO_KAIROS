from uuid import UUID
from models import ImageModel
from core.logging import get_logger

logger=get_logger(__name__)

class ImageService:
    def __init__(self,db_client:object,session_id:UUID):
        self.model=ImageModel(db_client=db_client,session_id=session_id)
        self.session_id=session_id

    async def insert_image_info(self,image):
        logger.info(f"Image insert requested | session_id={self.session_id}")
        try:
            result= await self.model.insert_image(image=image)
            logger.info(f"Image insert completed | image_id={result.Image_id} | session_id={self.session_id}")
            return result
        except Exception:
            logger.error(f"Image insert failed in service layer", exc_info=True)
            raise

    async def update_grad_cam(self,image_id:UUID,grad_cam_image):
        try:
            result=await self.model.update_gradcam_path(image_id=image_id,grad_cam_image=grad_cam_image)
            logger.info(f"GradCAM update completed | image_id={image_id}| session_id={self.session_id}")
            return result
        except Exception:
            logger.error(f"GradCAM update failed | image_id={image_id} | session_id={self.session_id}", exc_info=True)
            raise