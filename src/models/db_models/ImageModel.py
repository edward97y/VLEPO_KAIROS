from uuid import UUID
from .BaseDataModel import BaseDataModel
from ..db_schemas.eye_db_schemas import Images
from sqlalchemy import update

class ImageModel(BaseDataModel):
    def __init__(self,db_client:object,session_id:UUID):
        super().__init__(db_client=db_client)
        self.session_id=session_id

    async def insert_image(self,image):
        
        path=self.get_image_path()
        self.save_image(image=image,path=path)
        async with self.db_client() as session:
            async with session.begin():
               new_image=Images(image_type="EYE",image_path=path,Image_Session_id=self.session_id)
               
               session.add(new_image)
               await session.flush()
            return new_image
               
        
    async def update_gradcam_path(self, image_id:UUID,grad_cam_image):
        grad_cam_image_path=self.get_image_path()
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


