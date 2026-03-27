from models import UserFeatureModel
from uuid import UUID
class UserFeatureService:
    def __init__(self,db_client,session_id:UUID):
        self.models=UserFeatureModel(db_client=db_client)
        self.session_id=session_id

    async def get_user_feature_info(self):

        result=await self.models.get_user_feature(session_id=self.session_id)
        if not result:
            return None
        return result
    async def insert_user_info(self,user_feature:dict):

        result=await self.models.insert_user_feature(session_id=self.session_id,user_feature=user_feature)
        return result
   
