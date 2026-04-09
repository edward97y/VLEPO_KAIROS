from models import UserFeatureModel
from uuid import UUID
from core.logging import get_logger

logger=get_logger(__name__)

class UserFeatureService:
    def __init__(self,db_client,session_id:UUID):
        self.models=UserFeatureModel(db_client=db_client)
        self.session_id=session_id

    async def get_user_feature_info(self):
        logger.info(f"get user feature request | session_id={self.session_id}")
        try:
            result=await self.models.get_user_feature(session_id=self.session_id)
            if not result:
                logger.info(f"user doesn`t have features | session_id={self.session_id}")
                return None
            logger.info(f"get user feature complete | session_id={self.session_id}")
            return result
        except Exception:
            logger.error(f"get user feature failed | session_id={self.session_id} ",exc_info=True)
            raise
    async def insert_user_info(self,user_feature:dict):
        logger.info(f"insert user feature request | session_id={self.session_id}")
        try:
            result=await self.models.insert_user_feature(session_id=self.session_id,user_feature=user_feature)

            logger.info(f"insert user feature complete | session_id={self.session_id}")
            return result
        except Exception:
            logger.error(f"user feature insert failed | session_id={self.session_id} ",exc_info=True)
            raise
