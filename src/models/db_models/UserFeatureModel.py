from .BaseDataModel import BaseDataModel
from ..db_schemas.eye_db_schemas import User_Feature
import uuid
from sqlalchemy import select
class UserFeatureModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client)
    async def get_user_feature(self,session_id:uuid):
        async with self.db_client() as session:
            query=select(User_Feature).where(User_Feature.Feature_Session_id==session_id)
            result= await session.execute(query)
            return result.scalars().first()
        
    async def insert_user_feature(self,session_id:uuid,user_feature:dict):
        
        async with self.db_client() as session:
            async with session.begin():
                new_feature=User_Feature(Feature_Session_id=session_id,
                User_Feature=user_feature)
                session.add(new_feature)
                await session.flush()
            return new_feature
            