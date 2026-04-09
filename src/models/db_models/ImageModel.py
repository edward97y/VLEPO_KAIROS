from uuid import UUID
from .BaseDataModel import BaseDataModel
from ..db_schemas.eye_db_schemas import Images
from sqlalchemy import update
from core.logging import get_logger

logger=get_logger(__name__)
class ImageModel(BaseDataModel):
    def __init__(self,db_client:object,session_id:UUID):
        super().__init__(db_client=db_client)
        self.session_id=session_id

    async def insert_image(self,image):
        logger.info(f"inserting image |session_id={self.session_id}")
        try:
            path=self.get_image_path()
            self.save_image(image=image,path=path)
            async with self.db_client() as session:
                async with session.begin():
                   new_image=Images(image_type="EYE",image_path=path,Image_Session_id=self.session_id)

                   session.add(new_image)
                   await session.flush()
                logger.info(f"Image inserted | image_path={path}")
                return new_image
        except Exception:
            logger.error(f"insert image failed | session_id={self.session_id} ",exc_info=True)   
            raise    
        
    async def update_gradcam_path(self, image_id:UUID,grad_cam_image):
        grad_cam_image_path=self.get_image_path()
        try:
            self.save_image(image=grad_cam_image,path=grad_cam_image_path)
            async with self.db_client() as session:
                async with session.begin():

                    result=await session.execute(
                        update(Images)
                        .where(Images.Image_id == image_id)
                        .values(grad_cam_image_path=grad_cam_image_path)
                        .returning(Images)
                    )
                    update_row=result.scalar_one()
                    return update_row
        except Exception:
            logger.error(f"grad cam update failed | session_id={self.session_id} | image_id={image_id}",exc_info=True)
            raise

